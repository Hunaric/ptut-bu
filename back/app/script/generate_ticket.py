import os
import random
from io import BytesIO

import qrcode
from PIL import Image, ImageDraw, ImageFont

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.loan import Loan

# Dossier pour sauvegarder les tickets
TICKETS_DIR = "tickets"
os.makedirs(TICKETS_DIR, exist_ok=True)

# Polices (essaie de charger des polices système, sinon utilise la police par défaut)
def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

font_title = get_font(28, bold=True)
font_label = get_font(13, bold=True)
font_text = get_font(15)
font_small = get_font(12)


def hex_to_rgb(hex_color):
    """Convertit une couleur hex en RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_ticket_image(loan: Loan, override_ticket=False):
    """
    Génère un ticket moderne : 3/4 coloré (infos) + 1/4 foncé (QR code)
    """
    # Ticket à utiliser
    if loan.ticket and not override_ticket:
        ticket_value = loan.ticket
    else:
        import uuid
        ticket_value = str(uuid.uuid4())
        loan.ticket = ticket_value

    # Dimensions du ticket
    width, height = 900, 300
    
    # ==================== PALETTES DE COULEURS ====================
    
    # PALETTE 1 : Crème dominant avec accents marron (PLUS LISIBLE)
    color_bg = hex_to_rgb("#EEE6D8")           # Crème (fond principal - 3/4)
    color_dark = hex_to_rgb("#93441A")         # Marron foncé (partie droite - 1/4)
    color_accent = hex_to_rgb("#B67332")       # Marron moyen (accents)
    color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    color_text_secondary = hex_to_rgb("#B67332") # Marron moyen (labels)
    color_text_light = hex_to_rgb("#EEE6D8")   # Crème (texte sur fond foncé)
    color_qr = hex_to_rgb("#DAAB3A")           # Doré (QR code)
    
    # PALETTE 2 : Doré dominant avec texte foncé (ORIGINAL AMÉLIORÉ)
    # color_bg = hex_to_rgb("#DAAB3A")           # Doré (fond principal)
    # color_dark = hex_to_rgb("#93441A")         # Marron foncé (partie droite)
    # color_accent = hex_to_rgb("#B67332")       # Marron moyen (accents)
    # color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    # color_text_secondary = hex_to_rgb("#B67332") # Marron moyen (labels)
    # color_text_light = hex_to_rgb("#EEE6D8")   # Crème (texte sur fond foncé)
    # color_qr = hex_to_rgb("#DAAB3A")           # Doré (QR code)
    
    # PALETTE 3 : Gris clair dominant (TRÈS LISIBLE)
    # color_bg = hex_to_rgb("#e5e7e6")           # Gris clair (fond principal)
    # color_dark = hex_to_rgb("#93441A")         # Marron foncé (partie droite)
    # color_accent = hex_to_rgb("#DAAB3A")       # Doré (accents)
    # color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    # color_text_secondary = hex_to_rgb("#B67332") # Marron moyen (labels)
    # color_text_light = hex_to_rgb("#e5e7e6")   # Gris clair (texte sur fond foncé)
    # color_qr = hex_to_rgb("#DAAB3A")           # Doré (QR code)
    
    # PALETTE 4 : Crème + Marron moyen (CONTRASTE DOUX)
    # color_bg = hex_to_rgb("#EEE6D8")           # Crème (fond principal)
    # color_dark = hex_to_rgb("#B67332")         # Marron moyen (partie droite - moins foncé)
    # color_accent = hex_to_rgb("#DAAB3A")       # Doré (accents)
    # color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    # color_text_secondary = hex_to_rgb("#B67332") # Marron moyen (labels)
    # color_text_light = hex_to_rgb("#EEE6D8")   # Crème (texte sur fond foncé)
    # color_qr = hex_to_rgb("#DAAB3A")           # Doré (QR code)
    
    # PALETTE 5 : Mix Crème/Gris avec Doré
    # color_bg = hex_to_rgb("#EEE6D8")           # Crème (fond principal)
    # color_dark = hex_to_rgb("#93441A")         # Marron foncé (partie droite)
    # color_accent = hex_to_rgb("#DAAB3A")       # Doré (accents)
    # color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    # color_text_secondary = hex_to_rgb("#93441A") # Marron foncé (labels aussi)
    # color_text_light = hex_to_rgb("#e5e7e6")   # Gris clair (texte sur fond foncé)
    # color_qr = hex_to_rgb("#EEE6D8")           # Crème (QR code)
    
    # PALETTE 6 : Doré pâle avec texte très foncé (HAUTE LISIBILITÉ)
    # color_bg = hex_to_rgb("#EEE6D8")           # Crème (fond principal)
    # color_dark = hex_to_rgb("#93441A")         # Marron foncé (partie droite)
    # color_accent = hex_to_rgb("#DAAB3A")       # Doré (accents)
    # color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    # color_text_secondary = hex_to_rgb("#93441A") # Marron foncé (labels - plus de contraste)
    # color_text_light = hex_to_rgb("#DAAB3A")   # Doré (texte sur fond foncé)
    # color_qr = hex_to_rgb("#DAAB3A")           # Doré (QR code)
    
    # PALETTE 7 : Inversé - Marron clair dominant
    # color_bg = hex_to_rgb("#B67332")           # Marron moyen (fond principal)
    # color_dark = hex_to_rgb("#93441A")         # Marron foncé (partie droite)
    # color_accent = hex_to_rgb("#DAAB3A")       # Doré (accents)
    # color_text_primary = hex_to_rgb("#EEE6D8") # Crème (texte principal)
    # color_text_secondary = hex_to_rgb("#DAAB3A") # Doré (labels)
    # color_text_light = hex_to_rgb("#DAAB3A")   # Doré (texte sur fond foncé)
    # color_qr = hex_to_rgb("#DAAB3A")           # Doré (QR code)
    
    # PALETTE 8 : Gris + Doré (MODERNE ET LISIBLE)
    # color_bg = hex_to_rgb("#e5e7e6")           # Gris clair (fond principal)
    # color_dark = hex_to_rgb("#B67332")         # Marron moyen (partie droite)
    # color_accent = hex_to_rgb("#DAAB3A")       # Doré (accents)
    # color_text_primary = hex_to_rgb("#93441A") # Marron foncé (texte principal)
    # color_text_secondary = hex_to_rgb("#B67332") # Marron moyen (labels)
    # color_text_light = hex_to_rgb("#DAAB3A")   # Doré (texte sur fond foncé)
    # color_qr = hex_to_rgb("#EEE6D8")           # Crème (QR code)
    
    # ==============================================================
    
    # Créer l'image du ticket
    img = Image.new("RGB", (width, height), color=color_bg)
    draw = ImageDraw.Draw(img)
    
    # Partie foncée (1/4 à droite)
    black_start_x = int(width * 3 / 4)
    draw.rectangle([black_start_x, 0, width, height], fill=color_dark)
    
    # Ligne de séparation dentelée
    perforation_x = black_start_x
    for y in range(10, height - 10, 16):
        draw.ellipse([perforation_x - 5, y - 5, perforation_x + 5, y + 5], 
                     fill=color_dark)
    
    # === PARTIE COLORÉE - INFORMATIONS (3/4) ===
    margin_x = 35
    y = 25
    
    # Grand titre "TICKET"
    draw.text((margin_x, y), "TICKET", fill=color_text_primary, font=font_title)
    y += 38
    
    # Rectangle foncé pour le sous-titre avec accent
    draw.rectangle([margin_x, y, margin_x + 180, y + 24], fill=color_dark)
    draw.rectangle([margin_x, y, margin_x + 6, y + 24], fill=color_accent)
    draw.text((margin_x + 12, y + 5), "BILLET D'EMPRUNT", fill=color_text_light, font=font_small)
    y += 38
    
    # Emprunteur
    draw.text((margin_x, y), "EMPRUNTEUR", fill=color_text_secondary, font=font_label)
    y += 20
    borrower_name = f"{loan.borrower.account.prenom} {loan.borrower.account.nom}".upper()
    draw.text((margin_x + 5, y), borrower_name, fill=color_text_primary, font=font_text)
    y += 28
    
    # Livre
    draw.text((margin_x, y), "TITRE DU LIVRE", fill=color_text_secondary, font=font_label)
    y += 20
    book_title = loan.book.title[:45] + "..." if len(loan.book.title) > 45 else loan.book.title
    draw.text((margin_x + 5, y), book_title.upper(), fill=color_text_primary, font=font_text)
    y += 22
    author_text = f"Par {loan.book.author}"
    author_text = author_text[:50] + "..." if len(author_text) > 50 else author_text
    draw.text((margin_x + 5, y), author_text, fill=color_text_secondary, font=font_small)
    y += 30
    
    # Dates
    draw.text((margin_x, y), f"PRÊT: {loan.loan_date}", fill=color_text_secondary, font=font_small)
    y += 18
    draw.text((margin_x, y), f"RETOUR: {loan.due_date}", fill=color_text_primary, font=font_text)
    
    # Code-barres en bas (variations en haut, base en bas)
    barcode_y_base = height - 15  # Position de la base (en bas)
    for i in range(margin_x, black_start_x - 80, 4):
        bar_height = random.choice([10, 12, 14, 10, 12])
        if i % 8 < 6:  # 75% de barres
            # Dessiner du bas vers le haut
            draw.rectangle([i, barcode_y_base - bar_height, i + 2, barcode_y_base], 
                          fill=color_text_primary)
    
    # Numéro de prêt au-dessus du code-barres
    draw.text((margin_x, barcode_y_base - 30), f"Prêt N° {loan.id}", 
              fill=color_text_secondary, font=font_small)
    
    # === PARTIE FONCÉE - QR CODE (1/4) ===
    qr_size = 200  # Taille du QR code
    
    # Générer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=1,
    )
    qr.add_data(ticket_value)
    qr.make(fit=True)
    
    # QR code coloré sur fond foncé
    qr_img = qr.make_image(fill_color=color_qr, back_color=color_dark).convert("RGB")
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    # Centrer le QR code dans la partie foncée
    qr_x = black_start_x + (width - black_start_x - qr_size) // 2
    qr_y = (height - qr_size) // 2 - 10
    img.paste(qr_img, (qr_x, qr_y))
    
    # ID du prêt sous le QR
    id_text = f"#{loan.id}"
    try:
        bbox = draw.textbbox((0, 0), id_text, font=font_small)
        text_width = bbox[2] - bbox[0]
    except:
        text_width = len(id_text) * 7
    
    text_x = qr_x + (qr_size - text_width) // 2
    draw.text((text_x, qr_y + qr_size + 8), id_text, fill=color_text_light, font=font_small)
    
    # Sauvegarder le ticket
    filename = os.path.join(TICKETS_DIR, f"ticket_{loan.id}.png")
    img.save(filename, quality=95)
    print(f"✓ Ticket généré : {filename}")

    return filename


def main():
    db: Session = SessionLocal()
    try:
        loans = db.query(Loan).all()

        if not loans:
            print("⚠ Aucun prêt trouvé en base !")
            return

        # Choisir un prêt au hasard
        loan = random.choice(loans)
        print(f"📋 Génération du ticket pour le prêt ID {loan.id}")

        # Générer le ticket
        generate_ticket_image(loan, override_ticket=False)

        # Mettre à jour la base si un nouveau ticket a été généré
        db.add(loan)
        db.commit()
        print("✓ Ticket sauvegardé avec succès!")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()