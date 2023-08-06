This is a module to wrap some functions of XMM SAS into python and perform specialized spectral analysis.

It is meant to extract spectra and light curves from a single point source in the field of view from the MOS cameras. No support for RGS is present.

It works for PN in maging mode and MOS in both imaging (small and full window) and timing mode.

Esamples are wrapped into jupyter notebooks.

It assumes sas is in 
/opt/sas
and CCF is in
/opt/CalDB/ccf/

It assumes that you work in a location into which the ODF files are in a subfolder called 'odf'.

This has been used for the paper:
Ferrigno, Bozzo et al. (2020)

