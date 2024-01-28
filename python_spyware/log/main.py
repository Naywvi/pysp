import logging
import logging.handlers

def setup_logger():
    # Création d'un logger personnalisé
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Niveau de base pour le logging

    # Créer un handler pour écrire les logs dans un fichier
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.ERROR)  # Enregistrer les erreurs et plus grave

    # Créer un handler pour l'affichage à la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Afficher les infos et plus grave

    # Créer un formateur et l'ajouter aux handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Ajouter les handlers au logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def main():
    logger = setup_logger()

    # Utilisation du logger
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == "__main__":
    main()
