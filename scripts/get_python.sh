unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    MSYS_NT*)   machine=MsysNt;;
    *)          machine="UNKNOWN:${unameOut}"
esac

PYTHON_VENV="${VENV_CACHE}/${machine}/${BLENDER_VERSION}/Python-${PYTHON_REV}"

#rm -rf  "${VENV_CACHE}/${machine}"
#rm -rf  "${VENV_CACHE}/Mac"

mkdir -p "${VENV_CACHE}/${machine}"
ls "${VENV_CACHE}/${machine}"

if [ ${machine} == "MsysNt" ]; then
    choco install python --version ${PYTHON_REV}
    py -m venv --copies ${PYTHON_VENV}
else
   if [ ! -d "${PYTHON_VENV}" ]; then
        cd ${VENV_CACHE}/${machine}
        if [ ${machine} == "Mac" ]; then
            #brew update
            #brew upgrade libssl-dev openssl > logfile 2>&1
            #brew unlink openssl && brew link openssl --force
            brew install openssl xz
            CPPFLAGS="-I$(brew --prefix openssl)/include" \
            LDFLAGS="-L$(brew --prefix openssl)/lib" \
            pythonz install ${PYTHON_VENV}
        else
            sudo apt-get install libssl-dev openssl
        fi
        wget https://www.python.org/ftp/python/${PYTHON_REV}/Python-${PYTHON_REV}.tgz
        tar -zxvf Python-${PYTHON_REV}.tgz > logfile 2>&1
        cd Python-${PYTHON_REV}
        if [ ${machine} == "Mac" ]; then
            which python
#             ./configure > logfile 2>&1
#             make > logfile 2>&1
#             ./python.exe -m venv --copies ${PYTHON_VENV}
        else
            ./configure > logfile 2>&1
            make > logfile 2>&1
            ./python -m venv --copies ${PYTHON_VENV}
        fi
    fi
fi

if [ ${machine} == "MsysNt" ]; then
    source ${PYTHON_VENV}/Scripts/activate
else
    source ${PYTHON_VENV}/bin/activate
fi

python -m pip install pip yolk3k --upgrade
python -m yolk -l

which python
export PYTHON_RET=`python --version`
if [ "${PYTHON_RET}" != "Python ${PYTHON_REV}" ]; then
    echo "Wrong Python rev returned!"
    echo " ${PYTHON_RET} != Python ${PYTHON_REV}"
    exit 1
else
    echo "This is the expected version of Python:"
    echo ${PYTHON_RET}
fi
