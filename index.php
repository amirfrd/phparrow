<?php
define('API_KEY', 'Your Token');
$admin = '68747297';
function api($method,$datas=[]){
    $url = "https://api.telegram.org/bot".API_KEY."/".$method;
    $ch = curl_init();
    curl_setopt($ch,CURLOPT_URL,$url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($ch,CURLOPT_POSTFIELDS,$datas);
    $res = curl_exec($ch);
    if(curl_error($ch)){
        var_dump(curl_error($ch));
    }else{
        return json_decode($res);
    }
}
/*function apipwd($method,$datas=[]){
    $url = "https://api.pwrtelegram.xyz/bot".API_KEY."/".$method;
    $ch = curl_init();
    curl_setopt($ch,CURLOPT_URL,$url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($ch,CURLOPT_POSTFIELDS,$datas);
    $res = curl_exec($ch);
    if(curl_error($ch)){
        var_dump(curl_error($ch));
    }else{
        return json_decode($res);
    }
}*/
function req($url){
  $res = file_get_contents($url);
  return json_decode($res);
}
function curl($url) {
	$ch = curl_init();
	$timeout = 5;
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
	$data = curl_exec($ch);
	curl_close($ch);
	return $data;
}
function r($command,$text){
  $i = str_replace("$command","",$text);
  return str_replace(" ","",$i);
}

$server = "dbsserver";
$username = "usernamedb";
$password = "passworddb";
$dbs = "databasename";
$db = new mysqli($server, $username, $password, $dbs);
$content = file_get_contents("php://input");
$u = json_decode($content, true);
$from = $u['message']['from']['id'];
$banlist = $db->query('SELECT id FROM ban WHERE id='.$from);
if($u['message']['text'] and $banlist->num_rows == 0){
  $msg = $u['message']['message_id'];
  $text = $u['message']['text'];
  $chat_id = $u['message']['chat']['id'];
  if($text == '/start' or $text == '/help' or $text == '/help@Arrow_robot'){
    $check = $db->query('SELECT id FROM member WHERE id='.$chat_id);
    if($check->num_rows == 0){
      $db->query('INSERT INTO member (id) VALUES ('.$chat_id.')');
    }
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"
Hello I'm Arrow

Commands :

<b>1</b>> /help
<b>2</b>> /echo [text]
<b>3</b>> /ip [URL|ip]
<b>4</b>> /imdb [name]
<b>5</b>> /spotify [name track]
<b>6</b>> /qr [text]
<b>7</b>> /translate [text]      #text to fa
<b>8</b>> /loc [name City]
<b>9</b>> /calc [expression]
<b>10</b>> /cat
<b>11</b>> /tosticker     #by_reply
<b>12</b>> /tophoto       #by_reply
      ",
      'parse_mode'=>'HTML',
      'reply_markup'=>json_encode(array(
        'inline_keyboard'=>array(
          array(
            array('text'=>'Creator','url'=>'https://telegram.me/negative'),
            array('text'=>'Channel','url'=>'https://telegram.me/taylor_team')
          ),
          array(
            array('text'=>'فارسی 🇮🇷','callback_data'=>'fa')
          )
        )
      ))
    ));
  }
  elseif(preg_match('/^\/([Ee]cho) (.*)/s',$text)){
    preg_match('/^\/([Ee]cho) (.*)/s',$text,$match);
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>$match[2].'',
      'parse_mode'=>'HTML'
    ));
  }
  elseif(preg_match('/^\/([Ii]p) (.*)/',$text)){
    preg_match('/^\/([Ii]p) (.*)/s',$text,$match);
    $txt = urlencode($match[2]);
    $res = json_decode(file_get_contents('http://api.ipinfodb.com/v3/ip-city/?key=bd36e5c11b78ac040a0858df1df61b3ac9fe6d1717bfe073690617557dd9dc42&ip='.$txt.'&format=json'));
    api('sendLocation',array('chat_id'=>$chat_id,'latitude'=>$res->latitude,'longitude'=>$res->longitude));
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"ip : <code>".$res->ipAddress."</code>\nCountry : <b>".$res->countryCode." - ".$res->countryName."</b>",
      'parse_mode'=>'HTML'
    ));
  }
  elseif(preg_match('/^\/([Ii]mdb) (.*)/s',$text)){
    preg_match('/^\/([Ii]mdb) (.*)/s',$text,$match);
    $txt = urlencode($match[2]);
    $rs = json_decode(file_get_contents('http://www.omdbapi.com/?t='.$txt));
    if(!$rs->Error){
      api('sendMessage',array(
        'chat_id'=>$chat_id,
        'text'=>"<b>Title</b> : ".$rs->Title."\n\n<b>Year</b> : ".$rs->Year."\n<b>Runtime</b> : ".$rs->Runtime."\n<b>Language</b> : ".$rs->Language,
        'parse_mode'=>'HTML'
      ));
      if($rs->Poster){
        file_put_contents('poster.jpg',file_get_contents($rs->Poster));
        api('sendSticker',array(
          'chat_id'=>$chat_id,
          'sticker'=>new CURLFile('poster.jpg')
        ));
      }
    }else{
      api('sendMessage',array('chat_id'=>$chat_id,'text'=>"Movie not found!"));
    }
  }
  elseif(preg_match('/^\/([Ss]potify) (.*)/s',$text)){
    preg_match('/^\/(spotify) (.*)/s',$text,$match);
    $txt = urlencode($match[2]);
    $rs = json_decode(file_get_contents('https://api.spotify.com/v1/search?limit=1&type=track&q='.$txt));
    if($rs->tracks->items[0]->album->name){
      api('sendMessage',array(
        'chat_id'=>$chat_id,
        'text'=>"<b>Artists Name</b> : ".$rs->tracks->items[0]->artists[0]->name."\n<b>Name</b> : ".$rs->tracks->items[0]->name."\n",
        'parse_mode'=>'HTML'
      ));
      api('sendMessage',array('chat_id'=>$chat_id,'text'=>"Poster 😇👇"));
      api('sendChatAction',array(
        'chat_id'=>$chat_id,
        'action'=>'upload_photo'
      ));
      file_put_contents('poster.jpg',file_get_contents($rs->tracks->items[0]->album->images[0]->url));
      api('sendPhoto',array(
        'chat_id'=>$chat_id,
        'photo'=>new CURLFile('poster.jpg')
      ));
      api('sendChatAction',array(
        'chat_id'=>$chat_id,
        'action'=>"record_audio"
      ));
      file_put_contents('music.mp3',file_get_contents($rs->tracks->items[0]->preview_url));
      $title = $rs->tracks->items[0]->name;
      api('sendAudio',array(
        'chat_id'=>$chat_id,
        'audio'=>new CURLFile('music.mp3'),
        'title'=>"$title"
      ));
    }
  }
  elseif(preg_match('/^\/([q]r) (.*)/s',$text)){
    preg_match('/^\/([q]r) (.*)/s',$text,$mtch);
    $txt = urlencode($mtch[2]);
    file_put_contents('poster.jpg',file_get_contents('https://api.qrserver.com/v1/create-qr-code/?size=500x500&data='.$txt));
    api('sendPhoto',array(
      'chat_id'=>$chat_id,
      'photo'=>new CURLFile('poster.jpg')
    ));
  }
  elseif(preg_match('/^\/([t]ranslate) (.*)/s',$text)){
    preg_match('/^\/([t]ranslate) (.*)/s',$mtch);
    $txt = urlencode($mtch[2]);
    $rs = json_decode(file_get_contents('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20160119T111342Z.fd6bf13b3590838f.6ce9d8cca4672f0ed24f649c1b502789c9f4687a&format=plain&lang=fa&text='.$txt));
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"".$rs->text[0],
      'reply_to_message_id'=>$msg
    ));
  }
  elseif(preg_match('/^\/([l]oc)/s',$text)){
    preg_match('/^\/([l]oc)/s',$text,$mtch);
    $txt = urlencode($mtch[2]);
    $rs = json_decode(file_get_contents('http://maps.googleapis.com/maps/api/geocode/json?address='.$txt));
    $lat = $rs->results[0]->geometry->location->lat;
    $lng = $rs->results[0]->geometry->location->lng;
    api('sendLocation',array(
      'chat_id'=>$chat_id,
      'latitude'=>$lat,
      'longitude'=>$lng
    ));
  }
  elseif(preg_match('/^\/(calc) (.*)/s',$text)){
    preg_match('/^\/(calc) (.*)/s',$text,$mtch);
    $txt = urlencode($mtch[2]);
    $rs = file_get_contents('http://api.mathjs.org/v1/?expr='.$txt);
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"<code>".$rs."</code>",
      'parse_mode'=>'HTML'
    ));
  }
  elseif(preg_match('/^\/(cat)/s',$text)){
    file_put_contents('cat.jpg',file_get_contents('http://thecatapi.com/api/images/get?format=src&type=jpg'));
    api('sendPhoto',array(
      'chat_id'=>$chat_id,
      'photo'=>new CURLFile('cat.jpg')
    ));
  }
  elseif(preg_match('/^\/(bc) (.*)/s',$text) and $from == $admin){
    preg_match('/^\/(bc) (.*)/s',$text,$mtch);
    $txt = $mtch[2];
    $select = $db->query('SELECT id FROM member');
    while($rw = $select->fetch_assoc()){
      api('sendMessage',array(
        'chat_id'=>$rw['id'],
        'text'=>"$txt",
        'parse_mode'=>'HTML'
      ));
    }
  }
  elseif(preg_match('/^\/(ban) (.*)/s',$text) and $from == $admin){
    preg_match('/^\/(ban) (.*)/s',$text,$mtch);
    $txt = $mtch[2];
    $select = $db->query('SELECT id FROM ban WHERE id='.$txt);
    if($select->num_rows == 0){
      $db->query('INSERT INTO ban (id) VALUES ('.$txt.')');
    }
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"<b>Banned</b>",
      'parse_mode'=>'HTML'
    ));
  }
  elseif(preg_match('/^\/(unban) (.*)/s',$text) and $from == $admin){
    preg_match('/^\/(unban) (.*)/s',$text,$mtch);
    $txt = $mtch[2];
    $select = $db->query('SELECT id FROM ban WHERE id='.$txt);
    if($select->num_rows != 0){
      $db->query('DELETE FROM ban WHERE id='.$txt);
    }
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"<b>Unbanned</b>",
      'parse_mode'=>'HTML'
    ));
  }
  elseif(preg_match('/^\/([Ll]eave)/',$text) and $from == $admin){
    api('leaveChat',array(
      'chat_id'=>$chat_id
    ));
  }
  elseif(preg_match('/^\/([Ss]tats)/',$text) and $from == $admin){
    $chs = $db->query('SELECT id FROM member');
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"<b>Members : </b>".$chs->num_rows."\n",
      'parse_mode'=>'HTML'
    ));
  }
  elseif(preg_match('/^\/(reply) (.*)/s',$text) and $u['message']['reply_to_message']){
    preg_match('/^\/(reply) (.*)/s',$text,$match);
    $txt = $match[2];
    $rpid = $u['message']['reply_to_message']['message_id'];
    api('sendMessage',array(
      'chat_id'=>$chat_id,
      'text'=>"$txt",
      'parse_mode'=>'HTML',
      'reply_to_message_id'=>$rpid
    ));
  }
  elseif(preg_match('/^\/(tosticker)/',$text) and $u['message']['reply_to_message']){
    if($u['message']['reply_to_message']['photo'][3]){
      $file = $u['message']['reply_to_message']['photo'][3]['file_id'];
      $get = api('getfile',array('file_id'=>"$file"));
      $patch = $get->result->file_path;
      file_put_contents('sticker.png',file_get_contents('https://api.telegram.org/file/bot'.API_KEY.'/'.$patch));
      api('sendSticker',array(
        'chat_id'=>$chat_id,
        'sticker'=>new CURLFile('sticker.png')
      ));
    }elseif($u['message']['reply_to_message']['photo'][2]){
      $file = $u['message']['reply_to_message']['photo'][2]['file_id'];
      $get = api('getfile',array('file_id'=>"$file"));
      $patch = $get->result->file_path;
      file_put_contents('sticker.png',file_get_contents('https://api.telegram.org/file/bot'.API_KEY.'/'.$patch));
      api('sendSticker',array(
        'chat_id'=>$chat_id,
        'sticker'=>new CURLFile('sticker.png')
      ));
    }elseif($u['message']['reply_to_message']['photo'][1]){
      $file = $u['message']['reply_to_message']['photo'][1]['file_id'];
      $get = api('getfile',array('file_id'=>"$file"));
      $patch = $get->result->file_path;
      file_put_contents('sticker.png',file_get_contents('https://api.telegram.org/file/bot'.API_KEY.'/'.$patch));
      api('sendSticker',array(
        'chat_id'=>$chat_id,
        'sticker'=>new CURLFile('sticker.png')
      ));
    }
  }
  elseif(preg_match('/^\/(tophoto)/',$text) and $u['message']['reply_to_message']){
    if($u['message']['reply_to_message']['sticker']){
      $file = $u['message']['reply_to_message']['sticker']['file_id'];
      $get = api('getfile',array('file_id'=>"$file"));
      $patch = $get->result->file_path;
      file_put_contents('sticker.png',file_get_contents('https://api.telegram.org/file/bot'.API_KEY.'/'.$patch));
      api('sendPhoto',array(
        'chat_id'=>$chat_id,
        'photo'=>new CURLFile('sticker.png')
      ));
    }
  }
  /*if($u['message']['new_chat_member']){
    if($u['message']['from']['id'] != 68747297){
      $idc = $u['message']['chat']['id'];
      api('leaveChat',array(
        'chat_id'=>$idc
      ));
    }
  }*/
}elseif($banlist->num_rows != 0){
  api('sendMessage',array(
    'chat_id'=>$u['message']['chat']['id'],
    'text'=>"You Are Banned"
  ));
}
if($u['callback_query']){
  $id = $u['callback_query']['id'];
  $chat_id = $u['callback_query']['message']['chat']['id'];
  $msg = $u['callback_query']['message']['message_id'];
  $data = $u['callback_query']['data'];
  if($data == 'fa'){
    api('editMessageText',array(
      'chat_id'=>$chat_id,
      'message_id'=>$msg,
      'text'=>"
سلام من ارو هستم

دستورات :

<b>1</b>> /help
<b>2</b>> /echo [متن]
<b>3</b>> /ip [ادرس]
<b>4</b>> /imdb [اسم]
<b>5</b>> /spotify [نام ترک]
<b>6</b>> /qr [متن]
<b>7</b>> /translate [متن]
<b>8</b>> /loc [نام شهر]
<b>9</b>> /calc [expression]
<b>10</b>> /cat
<b>11</b>> /tosticker     #by_reply
<b>12</b>> /tophoto       #by_reply
      ",
      'parse_mode'=>'HTML',
      'reply_markup'=>json_encode(array(
        'inline_keyboard'=>array(
          array(
            array('text'=>'برگشت','callback_data'=>'bc')
          )
        )
      ))
    ));
  }if($data == 'bc'){
    api('editMessageText',array(
      'chat_id'=>$chat_id,
      'message_id'=>$msg,
      'text'=>"
Hello I'm Arrow

Commands :

<b>1</b>> /help
<b>2</b>> /echo [text]
<b>3</b>> /ip [URL|ip]
<b>4</b>> /imdb [name]
<b>5</b>> /spotify [name track]
<b>6</b>> /qr [text]
<b>7</b>> /translate [text]      #text to fa
<b>8</b>> /loc [name City]
<b>9</b>> /calc [expression]
<b>10</b>> /cat
<b>11</b>> /tosticker     #by_reply
<b>12</b>> /tophoto       #by_reply
      ",
      'parse_mode'=>'HTML',
      'reply_markup'=>json_encode(array(
        'inline_keyboard'=>array(
          array(
            array('text'=>'Creator','url'=>'https://telegram.me/negative'),
            array('text'=>'Channel','url'=>'https://telegram.me/taylor_team')
          ),
          array(
            array('text'=>"فارسی 🇮🇷",'callback_data'=>'fa')
          )
        )
      ))
    ));
  }
}
if($u['inline_query']){
  $id = $u['inline_query']['id'];
  $query = $u['inline_query']['query'];
  if($query){
    $txt = urlencode($query);
    api('answerInlineQuery',array(
      'inline_query_id'=>$id,
      'cache_time'=>1,
      'results'=>json_encode(array(
        array(
          'type'=>'photo',
          'id'=>base64_encode('1'),
          'photo_url'=>'http://apimeme.com/meme?meme=WTF&top='.$txt.'&bottom=',
          'thumb_url'=>'http://apimeme.com/meme?meme=WTF&top='.$txt.'&bottom='
        ),
        array(
          'type'=>'photo',
          'id'=>base64_encode('2'),
          'photo_url'=>'http://apimeme.com/meme?meme=What+Year+Is+It&top='.$txt.'&bottom=',
          'thumb_url'=>'http://apimeme.com/meme?meme=What+Year+Is+It&top='.$txt.'&bottom='
        ),
        array(
          'type'=>'photo',
          'id'=>base64_encode('3'),
          'photo_url'=>'http://apimeme.com/meme?meme=No+I+Cant+Obama&top='.$txt.'&bottom=',
          'thumb_url'=>'http://apimeme.com/meme?meme=No+I+Cant+Obama&top='.$txt.'&bottom='
        )
      ))
    ));

  }/*elseif(preg_match('/^(sticker) (.*)/',$query)){
    preg_match('/^(sticker) (.*)/',$query,$match);
    $txt = urlencode($match[2]);
    file_put_contents('sticker.png',file_get_contents('http://api.img4me.com/?text='.$txt.'&font=arial&fcolor=000000&size=30&bcolor=FFFFFF&type=png'));
    $gets = api('sendSticker',array(
      'chat_id'=>-170511242,
      'sticker'=>new CURLFile('sticker.png')
    ));
    $sc3 = $gets->result->sticker->file_id;
    api('answerInlineQuery',array(
      'inline_query_id'=>$id,
      'cache_time'=>1,
      'results'=>json_encode(array(
        array(
          'type'=>'sticker',
          'id'=>base64_encode('1'),
          'sticker_file_id'=>"$sc3"
        )
      ))
    ));
  }*/
}
$db->close();
