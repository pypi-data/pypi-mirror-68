import numpy as np
from soxs.spectra import Spectrum, ConvolvedSpectrum, \
    _generate_energies, Energies
from soxs.constants import erg_per_keV
from soxs.utils import parse_prng, parse_value
from soxs.instrument import AuxiliaryResponseFile
import h5py


class BackgroundSpectrum(Spectrum):
    _units = "photon/(cm**2*s*keV*arcmin**2)"
    def __init__(self, ebins, flux):
        super(BackgroundSpectrum, self).__init__(ebins, flux)

    @classmethod
    def from_spectrum(cls, spec, fov):
        """
        Create a background spectrum from a regular
        :class:`~soxs.spectra.Spectrum` object and the width
        of a field of view on a side.

        Parameters
        ----------
        spec : :class:`~soxs.spectra.Spectrum`
            The spectrum to be used.
        fov : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The width of the field of view on a side in 
            arcminutes.
        """
        fov = parse_value(fov, "arcmin")
        flux = spec.flux.value/fov/fov
        return cls(spec.flux.ebins.value, flux)

    def generate_energies(self, t_exp, area, fov, prng=None, 
                          quiet=False):
        """
        Generate photon energies from this background 
        spectrum given an exposure time, effective area, 
        and field of view.

        Parameters
        ----------
        t_exp : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The exposure time in seconds.
        area : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The effective area in cm**2. If one is creating 
            events for a SIMPUT file, a constant should be 
            used and it must be large enough so that a 
            sufficiently large sample is drawn for the ARF.
        fov : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The width of the field of view on a side in 
            arcminutes.
        prng : :class:`~numpy.random.RandomState` object, integer, or None
            A pseudo-random number generator. Typically will only 
            be specified if you have a reason to generate the same 
            set of random numbers, such as for a test. Default is None, 
            which sets the seed based on the system time.
        quiet : boolean, optional
            If True, log messages will not be displayed when 
            creating energies. Useful if you have to loop over 
            a lot of spectra. Default: False
        """
        t_exp = parse_value(t_exp, "s")
        fov = parse_value(fov, "arcmin")
        area = parse_value(area, "cm**2")
        prng = parse_prng(prng)
        rate = area*fov*fov*self.total_flux.value
        energy = _generate_energies(self, t_exp, rate, prng, quiet=quiet)
        flux = np.sum(energy)*erg_per_keV/t_exp/area
        energies = Energies(energy, flux)
        return energies

    def to_spectrum(self, fov):
        fov = parse_value(fov, "arcmin")
        flux = self.flux.value*fov*fov
        return Spectrum(self.ebins.value, flux)

    def __mul__(self, other):
        if isinstance(other, AuxiliaryResponseFile):
            return ConvolvedBackgroundSpectrum(self, other)
        else:
            return BackgroundSpectrum(self.ebins, other*self.flux)

    __rmul__ = __mul__


class InstrumentalBackgroundSpectrum(BackgroundSpectrum):
    _units = "photon/(s*keV*arcmin**2)"

    def __init__(self, ebins, flux, default_focal_length):
        super(BackgroundSpectrum, self).__init__(ebins, flux)
        self.default_focal_length = default_focal_length
 
    @classmethod
    def from_file(cls, filename, default_focal_length):
        """
        Read an instrumental background spectrum from 
        an ASCII or HDF5 file.

        If ASCII: accepts a file with two columns,
        the first being the center energy of the bin in 
        keV and the second being the spectrum in the
        appropriate units, assuming a linear binning 
        with constant bin widths.

        If HDF5: accepts a file with one array dataset, 
        named "spectrum", which is the spectrum in the 
        appropriate units, and two scalar datasets, 
        "emin" and "emax", which are the minimum and 
        maximum energies in keV.

        Parameters
        ----------
        filename : string
            The path to the file containing the spectrum.
        default_focal_length : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The default focal length of the instrument
            in meters. 
        """
        if filename.endswith(".h5"):
            f = h5py.File(filename, "r")
            flux = f["spectrum"][()]
            nbins = flux.size
            ebins = np.linspace(f["emin"][()], f["emax"][()], nbins+1)
            f.close()
        else:
            emid, flux = np.loadtxt(filename, unpack=True)
            de = np.diff(emid)[0]
            ebins = np.append(emid-0.5*de, emid[-1]+0.5*de)
        return cls(ebins, flux, default_focal_length)

    @classmethod
    def from_instrument(cls, instr_name):
        """
        Obtain an instrumental background spectrum corresponding
        to a registered instrument.

        Parameters
        ----------
        instr_name : string
            Name of the instrument in the instrument registry.
        """
        from soxs.instrument_registry import instrument_registry
        from soxs.background.instrument import instrument_backgrounds
        instr = instrument_registry[instr_name]
        return instrument_backgrounds[instr["bkgnd"]]

    def generate_energies(self, t_exp, fov, focal_length=None, 
                          prng=None, quiet=False):
        """
        Generate photon energies from this instrumental 
        background spectrum given an exposure time, 
        effective area, and field of view.

        Parameters
        ----------
        t_exp : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The exposure time in seconds.
        fov : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The width of the field of view on a side in 
            arcminutes.
        focal_length : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`, optional
            The focal length in meters. Default is to use
            the default focal length of the instrument
            configuration.
        prng : :class:`~numpy.random.RandomState` object, integer, or None
            A pseudo-random number generator. Typically will only 
            be specified if you have a reason to generate the same 
            set of random numbers, such as for a test. Default is None, 
            which sets the seed based on the system time. 
        quiet : boolean, optional
            If True, log messages will not be displayed when 
            creating energies. Useful if you have to loop over 
            a lot of spectra. Default: False
        """
        t_exp = parse_value(t_exp, "s")
        fov = parse_value(fov, "arcmin")
        prng = parse_prng(prng)
        if focal_length is None:
            focal_length = self.default_focal_length
        else:
            focal_length = parse_value(focal_length, "m")
        rate = fov*fov*self.total_flux.value
        rate *= (focal_length/self.default_focal_length)**2
        energy = _generate_energies(self, t_exp, rate, prng, quiet=quiet)
        flux = np.sum(energy)*erg_per_keV/t_exp
        energies = Energies(energy, flux)
        return energies

    def to_scaled_spectrum(self, fov, focal_length=None):
        from soxs.instrument import FlatResponse
        fov = parse_value(fov, "arcmin")
        if focal_length is None:
            focal_length = self.default_focal_length
        else:
            focal_length = parse_value(focal_length, "m")
        flux = self.flux.value*fov*fov
        flux *= (focal_length/self.default_focal_length)**2
        arf = FlatResponse(self.ebins.value[0], self.ebins.value[-1],
                           1.0, self.ebins.size-1)
        return ConvolvedSpectrum(Spectrum(self.ebins.value, flux), arf)

    def new_spec_from_band(self, emin, emax):
        """
        Create a new :class:`~soxs.spectra.Spectrum` object
        from a subset of an existing one defined by a particular
        energy band.

        Parameters
        ----------
        emin : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The minimum energy of the band in keV.
        emax : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The maximum energy of the band in keV.
        """
        emin = parse_value(emin, "keV")
        emax = parse_value(emax, 'keV')
        band = np.logical_and(self.ebins.value >= emin,
                              self.ebins.value <= emax)
        idxs = np.where(band)[0]
        ebins = self.ebins.value[idxs]
        flux = self.flux.value[idxs[:-1]]
        return InstrumentalBackgroundSpectrum(ebins, flux, 
                                              self.default_focal_length)

    def __mul__(self, other):
        if isinstance(other, AuxiliaryResponseFile):
            raise NotImplementedError
        else:
            return InstrumentalBackgroundSpectrum(self.ebins, other*self.flux,
                                                  self.default_focal_length)

    __rmul__ = __mul__


class ConvolvedBackgroundSpectrum(ConvolvedSpectrum):
    _units = "photon/(s*keV*arcmin**2)"

    def generate_energies(self, t_exp, fov, prng=None, 
                          quiet=False):
        """
        Generate photon energies from this convolved 
        background spectrum given an exposure time and 
        field of view.

        Parameters
        ----------
        t_exp : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The exposure time in seconds.
        fov : float, (value, unit) tuple, or :class:`~astropy.units.Quantity`
            The width of the field of view on a side 
            in arcminutes.
        prng : :class:`~numpy.random.RandomState` object, integer, or None
            A pseudo-random number generator. Typically will only 
            be specified if you have a reason to generate the same 
            set of random numbers, such as for a test. Default is None, 
            which sets the seed based on the system time. 
        quiet : boolean, optional
            If True, log messages will not be displayed when 
            creating energies. Useful if you have to loop over 
            a lot of spectra. Default: False
        """
        t_exp = parse_value(t_exp, "s")
        fov = parse_value(fov, "arcmin")
        prng = parse_prng(prng)
        rate = fov*fov*self.total_flux.value
        energy = _generate_energies(self, t_exp, rate, prng, quiet=quiet)
        earea = self.arf.interpolate_area(energy).value
        flux = np.sum(energy)*erg_per_keV/t_exp/earea.sum()
        energies = Energies(energy, flux)
        return energies
