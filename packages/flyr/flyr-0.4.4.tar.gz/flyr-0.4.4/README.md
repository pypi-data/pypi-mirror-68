# Flyr
Flyr is a library extracting thermal data from FLIR images written fully in Python, without depending on ExifTool.

Other solutions are wrappers around ExifTool to actually do the hard part of extracting the thermal data. Flyr is a reimplementation of the ExifTool's FLIR parser. Practically, this offers the following benefits:

* Faster decoding because no new process needs to be started and in-memory data does not need to be communicated to this other process
* Easier and robust installation and deployment, because `flyr.py` is not an external executable
* Simpler use (in my opinion): simply call `thermal = flyr.unpack(flir_file_path)` and done

## Installation

Flyr is installable through PyPi: `pip install flyr`.

Alternatively, download flyr.py and include in your source tree.

Flyr depends on three external packages, all installable through pip: `pip install numpy nptyping pillow`. Pillow does the conversion from PNG file to an array, nptyping allows for high quality array type annotations. Numpy provides the two dimensional array type containing the thermal data.

## Usage
Call `flyr.unpack` on a filepath to receive a numpy array with the thermal data. Alternatively, first open the file in binary mode for reading and and pass the the file handle to `flyr.unpack`.

```python
import flyr

flir_path = "/path/to/FLIR9121.jpg"  
thermal = flyr.unpack(flir_path)  # Reading directly

with open(flir_path, "rb") as flir_handle:  # In binary mode!
	thermal = flyr.unpack(flir_handle)  # Reading from file handle
```

Alternatively, if you already have the file in memory as a `BytesIO`, you can directly call `flyr.unpack` on that byte stream.

Lastly, flyr.py can be run as a script to unpack a single image:

```shell
$ ./flyr.py ./FLIR123l.jpg
```

## Status
Currently this library has been tested to work with:

* FLIR E5
* FLIR E8XT
* FLIR E53
* FLIR E75
* FLIR T630SC
* FLIR T660

However, the library is still in an early phase and lacks robust handling of inconsistent files. When it encounters such an image it immediately gives up raising a ValueError, while it could also do a best effort attempt to extract anyway. This is planned.

Camera's found not to work (yet):

* FLIR One
* FLIR E60BX
* FLIR Thermocam B400

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements
This code would not be possible without [ExifTool](https://exiftool.org/)'s efforts to [document](https://exiftool.org/TagNames/FLIR.html) the FLIR format.

## License
Flyr is licensed under [The European Union Public License](https://eupl.eu/) 1.2.
