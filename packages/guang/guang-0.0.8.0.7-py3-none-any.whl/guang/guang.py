import fire
import os
from guang.Utils.toolsFunc import path


def mie():
    origin_wd = os.getcwd()
    os.chdir(r"C:\Users\beidongjiedeguang\OneDrive\a_github\ScatteringLight")
    os.system("streamlit run app.py")
    os.chdir(origin_wd)

def lorenz():
    app_path = path(os.path.join(os.path.dirname(__file__), "app/compose/anim_demo.py"))
    os.system(f"streamlit run {app_path}")

def sawtooth():
    file_path = path(os.path.join(os.path.dirname(__file__), "app/compose/slider.py"))
    os.system(f"python {file_path}")

def geo():
    file_path = path(os.path.join(os.path.dirname(__file__), "geo/compose.py"))
    os.system(f"python {file_path}")

def multi_cvt2wav(PATH1, PATH2, FORMAT='*',sr=16000, n_cpu=None):
    """
    :arg PATH1: Input folder path
    :arg PATH2: Output folder path
    :arg FORMAT: Input voice format,  default all files
    :arg sr: Sample rate, default:16000
    :arg n_cpu: Number of multiple processes
    """
    from guang.Voice.convert import multi_cvt2wav as cvt
    cvt(PATH1, PATH2, FORMAT, sr, n_cpu)


def main():
    fire.Fire({
        'mie':mie,
        'lorenz':lorenz,
        "geo":geo,
        'sawtooth':sawtooth,
        'cvt2wav':multi_cvt2wav,

    })


if __name__ == "__main__":
    main()


