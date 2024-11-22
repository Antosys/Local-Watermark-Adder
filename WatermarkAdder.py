import os
from tkinter import filedialog, messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def add_watermark(pdf_path, watermark_text, output_path):
    try:
        # Créer une watermark temporaire
        watermark_file = "temp_watermark.pdf"
        create_watermark(watermark_text, watermark_file)

        # Charger le PDF existant et appliquer la watermark
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            page.merge_page(PdfReader(watermark_file).pages[0])
            writer.add_page(page)

        # Sauvegarder le nouveau fichier PDF
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        # Supprimer le fichier temporaire
        os.remove(watermark_file)
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de la watermark : {e}")
        return False


def create_watermark(text, output_path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    c = canvas.Canvas(output_path, pagesize=letter)

    width, height = letter
    c.setFont("Helvetica", 120)  # Utilisation de la police intégrée "Helvetica"
    c.setFillGray(0, alpha=0.2)  # Opacité réduite

    # Positionnement diagonal
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, text)

    c.save()


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_file_label.configure(text=os.path.basename(file_path))
        global selected_file
        selected_file = file_path


def process_pdf():
    if not selected_file:
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF.")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text.strip():
        messagebox.showerror("Erreur", "Veuillez entrer un texte de watermark.")
        return

    # Définir le chemin de sortie
    output_path = os.path.splitext(selected_file)[0] + "_filigrane.pdf"

    # Ajouter la watermark
    success = add_watermark(selected_file, watermark_text, output_path)
    if success:
        messagebox.showinfo("Succès", f"PDF avec filigrane généré : {output_path}")
    else:
        messagebox.showerror("Erreur", "Échec de l'ajout de la watermark.")


# Interface graphique avec customtkinter
root = CTk()
root.title("Filigrane Accor")
root.geometry("450x300")
root.resizable(False, False)

# Titre
title_label = CTkLabel(root, text="ACCOR Filigrane par Antoine", font=("Helvetica", 16))
title_label.pack(pady=10)

# Zone de texte pour entrer la watermark
watermark_entry = CTkEntry(root, placeholder_text="Entrez votre filigrane ici", font=("Helvetica", 12), width=250)
watermark_entry.pack(pady=10)

# Bouton pour sélectionner un fichier
select_button = CTkButton(
    master=root,
    text="Choisir un fichier PDF",
    corner_radius=10,
    command=select_file
)
select_button.pack(pady=10)

# Étiquette pour afficher le fichier sélectionné
input_file_label = CTkLabel(root, text="Aucun fichier sélectionné", font=("Helvetica", 10), text_color="gray")
input_file_label.pack(pady=5)

# Bouton pour traiter le PDF
process_button = CTkButton(
    master=root,
    text="Générer le PDF",
    corner_radius=10,
    command=process_pdf
)
process_button.pack(pady=20)

selected_file = None

# Lancement de l'application
root.mainloop()
