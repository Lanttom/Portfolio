<?php
require_once 'config.php';

$database = new Database('localhost', 'root', '', 'portfolio');
$pdo = $database->connect();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $subject = htmlspecialchars($_POST['subject']);
    $message = htmlspecialchars($_POST['message']);

    $sql = "
    INSERT INTO contacts (name, email, subject, message) VALUES
        ('$name', '$email', '$subject', '$message');
    ";

    $pdo->query($sql);
    header('Location: index.html');
}
