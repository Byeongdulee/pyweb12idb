# pyweb12idb
 A python tool to retrieve the APS 12IDB 1D data
 Only the current beamline users can download data using this tool and a passcode is required.

# Requirement
 python version 3 and higher.
 You will need to install matplotlib and numpy using pip install.

# Example
 1. Download the code to a directory, let's say c:\mycode\pyweb12idb
 2. Start python and add the path.
    
    $ python
    
    >import sys
    
    >sys.path.append("c:/mycode")
    
    >import pyweb12idb as wb
 3. If you know your passcode, for example, "Lee_01", you can proceed. When you want data files with the file index 1;
    
    >wb.get("Lee_01", 1)
    
    This will download all 1D files with the file index 1. There can be many files with the same file index with different extension numbers.
 4. If you want to a specific extension number, for example 3 (This means your 2D file name is something like "Saaa_bbb_00001_00003.tif");
    
    >wb.get("Lee_01", 1, 3)
 5. For multiple extension numbers, you can do like
    
    >wb.get("Lee_01", 1, [1,3,4,6])
 6. To plot these data,
    
    >wb.plot()
 7. To save data under your current folder
    
    >wb.save()
