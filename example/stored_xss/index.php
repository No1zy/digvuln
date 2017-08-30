<?php
session_start();
if (!isset($_SESSION["name"])) header("Location: ./login.php"); 


?>
<h1>Home Page</h1>
<a href="./sink.php">welcome page</a>
<a href="#">Logout</a>
