<?php

class Database
{
    // All variables of the connection
    private $host;
    private $user;
    private $password;
    private $database;
    private $pdo;

    // Constructor of the class
    public function __construct($host, $user, $password, $database) {
        $this->host = $host;
        $this->user = $user;
        $this->password = $password;
        $this->database = $database;
    }

    // Method to connect at the BDD
    public function connect() {
        try {
            $dsn = "mysql:host={$this->host};dbname={$this->database}";
            $options = array(
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            );
            $this->pdo = new PDO($dsn, $this->user, $this->password, $options);
            // echo "Succesful connexion";
        } catch (PDOException $e) {
            die("Connexion failed : " . $e->getMessage());
        }
        return $this->pdo;
    }
}
?>