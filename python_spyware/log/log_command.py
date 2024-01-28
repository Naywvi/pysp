import logging
import argparse

def setup_logger(log_level, log_file):
    # Création d'un logger personnalisé
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Créer un handler pour écrire les logs dans un fichier
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.ERROR)

    # Créer un handler pour l'affichage à la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Créer un formateur et l'ajouter aux handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Ajouter les handlers au logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def parse_arguments():
    parser = argparse.ArgumentParser(description="Example Script with Logging and Argparse")
    parser.add_argument("-l", "--log", help="Set the logging level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument("-f", "--logfile", help="Log file path", default="app.log")

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    log_level = getattr(logging, args.log.upper(), None)
    log_file = args.logfile

    logger = setup_logger(log_level, log_file)

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == "__main__":
    main()
    
# python logging_argparse_example.py --log DEBUG pour définir le niveau de log sur DEBUG.
# python logging_argparse_example.py --log ERROR --logfile error.log pour enregistrer uniquement les erreurs dans error.log.
