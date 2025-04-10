import os
import time
import webbrowser

import numpy as np
import pyautogui

# Configuration de PyAutoGUI
pyautogui.FAILSAFE = True  # Déplacez la souris dans un coin pour arrêter le script
pyautogui.PAUSE = 1  # Pause entre les actions

class AmazonBot:
    def __init__(self):
        # Créer le dossier pour les images de référence
        if not os.path.exists('reference_images'):
            os.makedirs('reference_images')

    def wait_and_click_image(self, image_name, confidence=0.8, timeout=10):
        """Attend qu'une image apparaisse à l'écran et effectue un clic avec mouseup/mousedown"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(f'reference_images/{image_name}.png', confidence=confidence)
                if location:
                    # Calculer le centre de l'image
                    center_x = location.left + location.width // 2
                    center_y = location.top + location.height // 2
                    
                    # Déplacer la souris vers la position avec un mouvement naturel
                    pyautogui.moveTo(center_x, center_y, duration=0.5 + np.random.random() * 0.5)
                    
                    # Ajouter un petit délai aléatoire avant le clic
                    time.sleep(0.1 + np.random.random() * 0.3)
                    
                    # Effectuer le clic avec mouseup/mousedown
                    pyautogui.mouseDown()
                    time.sleep(0.05 + np.random.random() * 0.1)  # Délai aléatoire entre down et up
                    pyautogui.mouseUp()
                    
                    return True
            except:
                pass
            time.sleep(0.5)
        return False

    def check_product_availability(self, product_url):
        """Vérifie la disponibilité d'un produit"""
        try:
            webbrowser.open(product_url)
            time.sleep(5)  # Attendre le chargement de la page

            # Chercher l'indicateur de disponibilité
            if self.wait_and_click_image('in_stock_indicator', timeout=5):
                return True
            return False

        except Exception as e:
            print(f"Erreur lors de la vérification de la disponibilité: {str(e)}")
            return False

    def add_to_cart(self):
        """Ajoute le produit au panier"""
        try:
            if self.wait_and_click_image('add_to_cart_button'):
                time.sleep(2)  # Attendre que le produit soit ajouté au panier
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de l'ajout au panier: {str(e)}")
            return False

    def checkout(self):
        """Procède au paiement"""
        try:
            if self.wait_and_click_image('checkout_button'):
                time.sleep(2)
                return True
            return False
        except Exception as e:
            print(f"Erreur lors du paiement: {str(e)}")
            return False

def capture_reference_images():
    """Capture les images de référence nécessaires pour le bot"""
    print("Mode capture d'images de référence")
    print("Placez votre souris sur chaque élément et appuyez sur 'c' pour capturer")
    print("Appuyez sur 'q' pour quitter")
    
    elements = [
        'in_stock_indicator',
        'add_to_cart_button',
        'checkout_button'
    ]

    for element in elements:
        input(f"Prêt à capturer {element}. Appuyez sur Entrée pour continuer...")
        time.sleep(3)  # Donner du temps pour positionner la souris
        screenshot = pyautogui.screenshot()
        screenshot.save(f'reference_images/{element}.png')
        print(f"Image {element} capturée!")

def main():
    bot = AmazonBot()
    
    # Liste des URLs des produits à surveiller
    product_urls = [
        # Ajoutez vos URLs de produits ici
    ]
    
    # Demander si l'utilisateur veut capturer des images de référence
    if input("Voulez-vous capturer des images de référence ? (o/n): ").lower() == 'o':
        capture_reference_images()
        return

    try:
        print("Bot démarré - surveillance des produits...")
        
        while True:
            for url in product_urls:
                if bot.check_product_availability(url):
                    print(f"Produit disponible: {url}")
                    if bot.add_to_cart():
                        if bot.checkout():
                            print("Achat effectué avec succès!")
                            return
                
                # Attendre 5 minutes avant de vérifier à nouveau
                time.sleep(300)
    except KeyboardInterrupt:
        print("\nArrêt du bot...")

if __name__ == "__main__":
    main() 