from supabase import create_client,Client

# Tes informations Supabase
#url = "https://cdbtkiygrvtzozuacsmh.supabase.co"  # Ton URL Supabase
url ="http://localhost:54321"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"                # Ta clé API publique
supabase: Client = create_client(url, key)

data = {"nom": "jean",
        "prenom": "jean@example.com",
        "date_naissance": "10/10/2003",
        "lieu_naissance": "Angodona", "domicile":"IIIB62D Andoharanofotsy",
        "arrondissement":"Andoharanofotsy", "profession":"mpianatra", "image":"10000"}
response = supabase.table("client").insert(data).execute()
print(response.data)

