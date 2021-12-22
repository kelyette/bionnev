from main_window import Gui
import yaml

def main():

    with open("parameters/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    default_envrule = config["default_envrule"]
    default_cellrule = config["default_cellrule"]
    default_plotrule = config["default_plotrule"]

    gui = Gui(default_envrule, default_cellrule, default_plotrule)

    gui.start()

if __name__ == '__main__':
    main()