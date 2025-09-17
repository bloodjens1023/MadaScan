<?php
// ⚡ Configuration Supabase
$supabase_url ="http://localhost:54321"
$supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"               
$table_name   = "users"; // ta table

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nom            = $_POST['nom'];
    $prenom         = $_POST['prenom'];
    $date_naissance = $_POST['date_naissance'];
    $lieu_naissance = $_POST['lieu_naissance'];
    $domicile       = $_POST['domicile'];
    $arrondissement = $_POST['arrondissement'];
    $profession     = $_POST['profession'];

    // Vérification de l'image
    if (isset($_FILES['image']) && $_FILES['image']['error'] === 0) {
        $targetDir = "img/";
        if (!is_dir($targetDir)) {
            mkdir($targetDir, 0777, true);
        }

        $photoName = uniqid() . "_" . basename($_FILES["image"]["name"]);
        $targetFilePath = $targetDir . $photoName;

        if (move_uploaded_file($_FILES["image"]["tmp_name"], $targetFilePath)) {
            
            // Données à insérer dans Supabase
            $data = [
                "nom"            => $nom,
                "prenom"         => $prenom,
                "date_naissance" => $date_naissance,
                "lieu_naissance" => $lieu_naissance,
                "domicile"       => $domicile,
                "arrondissement" => $arrondissement,
                "profession"     => $profession,
                "image"          => $targetFilePath  // chemin du fichier
            ];

            // Requête Supabase
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "$supabase_url/rest/v1/$table_name");
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER, [
                "Content-Type: application/json",
                "apikey: $supabase_key",
                "Authorization: Bearer $supabase_key",
                "Prefer: return=representation"
            ]);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

            $response = curl_exec($ch);
            $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);

            if ($httpcode == 201) {
                echo "✅ Utilisateur ajouté avec succès !";
            } else {
                echo "❌ Erreur Supabase : $response";
            }
        } else {
            echo "Erreur lors de l'upload de l'image.";
        }
    } else {
        echo "Veuillez sélectionner une image valide.";
    }
}
?>

<!-- Formulaire HTML -->
<form method="POST" enctype="multipart/form-data">
    Nom: <input type="text" name="nom" required><br>
    Prénom: <input type="text" name="prenom" required><br>
    Date de naissance: <input type="date" name="date_naissance" required><br>
    Lieu de naissance: <input type="text" name="lieu_naissance" required><br>
    Domicile: <input type="text" name="domicile" required><br>
    Arrondissement: <input type="text" name="arrondissement" required><br>
    Profession: <input type="text" name="profession" required><br>
    Image: <input type="file" name="image" required><br>
    <button type="submit">Ajouter</button>
</form>
