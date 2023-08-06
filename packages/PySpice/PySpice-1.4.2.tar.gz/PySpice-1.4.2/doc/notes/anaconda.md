# Anaconda

* https://www.anaconda.com/products/individual
* https://docs.conda.io/en/latest

	* https://en.wikipedia.org/wiki/Anaconda_(Python_distribution)

## Miniconda

Miniconda is a free minimal installer for conda. It is a small, bootstrap version of Anaconda that
includes only conda, Python, the packages they depend on, and a small number of other useful
packages, including pip, zlib and a few others.

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

## Conda-build

Conda-build contains commands and tools to use conda to build your own packages. It also provides
helpful tools to constrain or pin versions in recipes. Building a conda package requires installing
conda-build and creating a conda recipe. You then use the conda build command to build the conda
package from the conda recipe.

## Anaconda Cloud

* [AncondaCloud](https://anaconda.org)

* https://anaconda.org/conda-forge/ngspice

```
ldd /usr/lib64/libngspice.so.0
    linux-vdso.so.1 (0x00007ffdce5fa000)
    libdl.so.2 => /lib64/libdl.so.2 (0x00007fe64812a000)
    libncurses.so.6 => /lib64/libncurses.so.6 (0x00007fe6480fd000)
    libtinfo.so.6 => /lib64/libtinfo.so.6 (0x00007fe6480ce000)
    libm.so.6 => /lib64/libm.so.6 (0x00007fe647f88000)
    libpthread.so.0 => /lib64/libpthread.so.0 (0x00007fe647f67000)
    libreadline.so.8 => /lib64/libreadline.so.8 (0x00007fe647f12000)
    libgomp.so.1 => /lib64/libgomp.so.1 (0x00007fe647ed6000)
    libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007fe647ebc000)
    libc.so.6 => /lib64/libc.so.6 (0x00007fe647cf6000)
    /lib64/ld-linux-x86-64.so.2 (0x00007fe648a8f000)
```

```
(base) fabrice@isis:.../miniconda3>conda install -c conda-forge ngspice

Collecting package metadata (current_repodata.json): done
Solving environment: failed with initial frozen solve. Retrying with flexible solve.
Solving environment: done
Collecting package metadata (repodata.json): done
Solving environment: failed with initial frozen solve. Retrying with flexible solve.
Solving environment: done

## Package Plan ##

  environment location: /opt/python-virtual-env/miniconda3

  added / updated specs:
    - ngspice


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    _libgcc_mutex-0.1          |      conda_forge           3 KB  conda-forge
    _openmp_mutex-4.5          |            0_gnu         435 KB  conda-forge
    ca-certificates-2020.4.5.1 |       hecc5488_0         146 KB  conda-forge
    certifi-2020.4.5.1         |   py37hc8dfbb8_0         151 KB  conda-forge
    conda-4.8.3                |   py37hc8dfbb8_1         3.0 MB  conda-forge
    gettext-0.19.8.1           |    hc5be6a0_1002         3.6 MB  conda-forge
    libgcc-ng-9.2.0            |       h24d8f2e_2         8.2 MB  conda-forge
    libgomp-9.2.0              |       h24d8f2e_2         816 KB  conda-forge
    libuuid-2.32.1             |    h14c3975_1000          26 KB  conda-forge
    libxcb-1.13                |    h14c3975_1002         396 KB  conda-forge
    ncurses-6.1                |    hf484d3e_1002         1.3 MB  conda-forge
    ngspice-31                 |       hcee41ef_0         4.8 MB  conda-forge
    openssl-1.1.1g             |       h516909a_0         2.1 MB  conda-forge
    pthread-stubs-0.4          |    h14c3975_1001           5 KB  conda-forge
    python-3.7.6               |h8356626_5_cpython        52.9 MB  conda-forge
    python_abi-3.7             |          1_cp37m           4 KB  conda-forge
    readline-8.0               |       hf8c457e_0         441 KB  conda-forge
    tk-8.6.10                  |       hed695b0_0         3.2 MB  conda-forge
    xorg-kbproto-1.0.7         |    h14c3975_1002          26 KB  conda-forge
    xorg-libice-1.0.10         |       h516909a_0          57 KB  conda-forge
    xorg-libsm-1.2.3           |    h84519dc_1000          25 KB  conda-forge
    xorg-libx11-1.6.9          |       h516909a_0         918 KB  conda-forge
    xorg-libxau-1.0.9          |       h14c3975_0          13 KB  conda-forge
    xorg-libxaw-1.0.13         |    h14c3975_1002         373 KB  conda-forge
    xorg-libxdmcp-1.1.3        |       h516909a_0          18 KB  conda-forge
    xorg-libxext-1.3.4         |       h516909a_0          51 KB  conda-forge
    xorg-libxmu-1.1.3          |       h516909a_0          90 KB  conda-forge
    xorg-libxpm-3.5.13         |       h516909a_0          63 KB  conda-forge
    xorg-libxt-1.1.5           |    h516909a_1003         367 KB  conda-forge
    xorg-xextproto-7.3.0       |    h14c3975_1002          27 KB  conda-forge
    xorg-xproto-7.0.31         |    h14c3975_1007          72 KB  conda-forge
    ------------------------------------------------------------
                                           Total:        83.6 MB

The following NEW packages will be INSTALLED:

  _openmp_mutex      conda-forge/linux-64::_openmp_mutex-4.5-0_gnu
  gettext            conda-forge/linux-64::gettext-0.19.8.1-hc5be6a0_1002
  libgomp            conda-forge/linux-64::libgomp-9.2.0-h24d8f2e_2
  libuuid            conda-forge/linux-64::libuuid-2.32.1-h14c3975_1000
  libxcb             conda-forge/linux-64::libxcb-1.13-h14c3975_1002
  ngspice            conda-forge/linux-64::ngspice-31-hcee41ef_0
  pthread-stubs      conda-forge/linux-64::pthread-stubs-0.4-h14c3975_1001
  python_abi         conda-forge/linux-64::python_abi-3.7-1_cp37m
  xorg-kbproto       conda-forge/linux-64::xorg-kbproto-1.0.7-h14c3975_1002
  xorg-libice        conda-forge/linux-64::xorg-libice-1.0.10-h516909a_0
  xorg-libsm         conda-forge/linux-64::xorg-libsm-1.2.3-h84519dc_1000
  xorg-libx11        conda-forge/linux-64::xorg-libx11-1.6.9-h516909a_0
  xorg-libxau        conda-forge/linux-64::xorg-libxau-1.0.9-h14c3975_0
  xorg-libxaw        conda-forge/linux-64::xorg-libxaw-1.0.13-h14c3975_1002
  xorg-libxdmcp      conda-forge/linux-64::xorg-libxdmcp-1.1.3-h516909a_0
  xorg-libxext       conda-forge/linux-64::xorg-libxext-1.3.4-h516909a_0
  xorg-libxmu        conda-forge/linux-64::xorg-libxmu-1.1.3-h516909a_0
  xorg-libxpm        conda-forge/linux-64::xorg-libxpm-3.5.13-h516909a_0
  xorg-libxt         conda-forge/linux-64::xorg-libxt-1.1.5-h516909a_1003
  xorg-xextproto     conda-forge/linux-64::xorg-xextproto-7.3.0-h14c3975_1002
  xorg-xproto        conda-forge/linux-64::xorg-xproto-7.0.31-h14c3975_1007

The following packages will be UPDATED:

  ca-certificates     pkgs/main::ca-certificates-2020.1.1-0 --> conda-forge::ca-certificates-2020.4.5.1-hecc5488_0
  conda                       pkgs/main::conda-4.8.3-py37_0 --> conda-forge::conda-4.8.3-py37hc8dfbb8_1
  libgcc-ng           pkgs/main::libgcc-ng-9.1.0-hdf63c60_0 --> conda-forge::libgcc-ng-9.2.0-h24d8f2e_2
  python                 pkgs/main::python-3.7.6-h0371630_2 --> conda-forge::python-3.7.6-h8356626_5_cpython
  readline               pkgs/main::readline-7.0-h7b6447c_5 --> conda-forge::readline-8.0-hf8c457e_0
  tk                         pkgs/main::tk-8.6.8-hbc83047_0 --> conda-forge::tk-8.6.10-hed695b0_0

The following packages will be SUPERSEDED by a higher-priority channel:

  _libgcc_mutex           pkgs/main::_libgcc_mutex-0.1-main --> conda-forge::_libgcc_mutex-0.1-conda_forge
  certifi              pkgs/main::certifi-2020.4.5.1-py37_0 --> conda-forge::certifi-2020.4.5.1-py37hc8dfbb8_0
  ncurses                 pkgs/main::ncurses-6.2-he6710b0_0 --> conda-forge::ncurses-6.1-hf484d3e_1002
  openssl              pkgs/main::openssl-1.1.1g-h7b6447c_0 --> conda-forge::openssl-1.1.1g-h516909a_0


Proceed ([y]/n)? n


CondaSystemExit: Exiting.
```
