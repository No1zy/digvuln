
<?php
header ( "X-XSS-Protection: 0" );
?>
<h2>名前を入力してください</h2>
<form method="post">
<input type="text" name="name">
<input type="submit" value="送信">
</form>

<a href="./sink.php">名前確認</a>
<?php 
if ( isset($_POST["name"]) ){
    session_start();
    $_SESSION["name"] = $_POST["name"];
    header("Location: ./index.php");
}
?>

