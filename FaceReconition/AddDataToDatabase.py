from supabase import create_client, Client

# Tes informations Supabase
url ="http://localhost:54321"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"                # Ta clé API publique

supabase: Client = create_client(url, key)


def ajout_client(nom, prenom, date_naissance,lieu_naissance, domicile, arrondissement, profession, image):

    data = {"nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "lieu_naissance": lieu_naissance, "domicile": domicile,
            "arrondissement": arrondissement,
            "profession": profession, "image": image}
    response = supabase.table("client").insert(data).execute()

def selection_client(idphoto):
    response = supabase.table("client").select("*").eq("image", idphoto).execute()
    return response.data




