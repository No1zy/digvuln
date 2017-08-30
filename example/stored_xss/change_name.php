<?php
session_start();
if (!isset($_SESSION["name"])) header("Location: ./login.php"); 

?>
<h2>変更する名前を入力してください</h2>
<form method="post">
<input type="text" name="name">
<input type="submit" value="送信">
</form>

<a href="./sink.php">名前確認</a>
<?php 
if ( isset($_POST["name"]) ){
    $_SESSION["name"] = $_POST["name"];
}
?>
