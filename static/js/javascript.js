window.addEventListener('DOMContentLoaded', function(){
  // パスワードとボタンのHTMLを取得
  let btn_passview = document.getElementById("display");
  let input_pass = document.getElementById("pass");
  // ボタンのイベントリスナーを設定
  btn_passview.addEventListener("click", (e)=>{
    // ボタンの通常の動作をキャンセル（フォーム送信をキャンセル）
    e.preventDefault();
    // パスワード入力欄のtype属性を確認
    if( input_pass.type === 'password' ) {
      // パスワードを表示する
      input_pass.type = 'text';
      btn_passview.textContent = '非表示';
    } else {
      // パスワードを非表示にする
      input_pass.type = 'password';
      btn_passview.textContent = '表示';
    }
  });
});
