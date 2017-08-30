
<h2>Please login admin.</h2>
<p>id: test<br>
password: test</p>

<form method="post">
    <p><label>id: <input type="text" name="id"></label></p>
    <p><label>password: <input type="password" name="password"></label></p>
    <p><input type="submit" value="ログイン"></p>
</form>
<?php
if (!isset($_POST["password"]) && !isset($_POST["id"])){
    echo "id とpasswordを入力してください";
    return;
}
$password = $_POST["password"];
$id = $_POST["id"];

$mysqli = new mysqli("localhost", "root", "", "rensyuu3");

if ($mysqli->connect_error) {
    echo $mysqli->connect_error;
    exit();
} else {
    $mysqli->set_charset("utf8");
}

$sql = "SELECT user_id FROM users WHERE user_id = '$id' AND password = '$password'";
if($result = $mysqli->query($sql)){
    $row = $result->fetch_assoc();
    echo "こんにちは！ " . $row["user_id"] . " さん<br>";
}

// DB接続を閉じる
$mysqli->close();

?>
