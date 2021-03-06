var myGamePiece;
var myBackground;
function startGame() {

    myGamePiece = new component(90, 60, "/static/img.png", 280, 175, "image");
    myBackground = new component(350, 350, "/static/map/Map3.jpg", 0, 0, "image");
    myGameArea.start();
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 350;
        this.canvas.height = 350;

        this.context = this.canvas.getContext("2d");
        var container_canvas = document.getElementById("container_canvas");
        container_canvas.insertBefore(this.canvas, container_canvas.childNodes[0]);
        this.frameNo = 0;
        this.interval = setInterval(updateGameArea, 20);
        window.addEventListener('keydown', function (e) {
      myGameArea.key = e.keyCode;
    })
    window.addEventListener('keyup', function (e) {
      myGameArea.key = false;
    })
  },
    stop : function() {
        clearInterval(this.interval);
    },
    clear : function() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}
function component(width, height, color, x, y, type) {
    this.type = type;
    if (type == "image") {
        this.image = new Image();
        this.image.src = color;
    }
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;
    this.x = x;
    this.y = y;
    this.update = function() {
        ctx = myGameArea.context;
        if (type == "image") {
            ctx.drawImage(this.image,
                this.x,
                this.y,
                this.width, this.height);
        } else {
            ctx.fillStyle = color;
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }
    this.newPos = function() {
        this.x += this.speedX;
        this.y += this.speedY;
    }
}

//Update the game area
function updateGameArea() {
    myGameArea.clear();
    myBackground.newPos();
    myBackground.update();
    myGamePiece.newPos();
    myGamePiece.update();
}

//move upwards in map
function moveup() {
    myGamePiece.speedY = -1;
}

//move downwards in map
//"Turn left + forward"
//"Turn Right + reverse"
function movedown() {
    myGamePiece.speedY = 1;
}

//move left in map
//Equivalent to "forward"
function moveleft() {
    myGamePiece.speedX = -1;
}

//move right in map
//Equivalent to "reverse"
function moveright() {
    myGamePiece.speedX = 1;
}

//stop moving
function clearmove() {
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;
}




//combining with send command button
function validate() {
  var get_data=document.getElementById("div2"); //get "sent" commands from div2
  textContent = get_data.textContent; //get text content only
  readTextFile("/static/quiz1.txt", textContent); //compare with answer key

}

//TAKE NOTE of this!!!!!!

function send() {
  var get_data=document.getElementById("div2"); //get "sent" commands from div2
  textContent = get_data.textContent; //get text content only
  var stringArray = textContent.split(/(\s+\s+)/); //split elements into array
  var newArr = stringArray.filter(function(entry) { return entry.trim() != ''; }) //remove empty strings

  //remove whitespaces at the ends of each element
  for (let i=0; i < newArr.length; i++){
    newArr[i] = newArr[i].trim();
  }

  //for debugging
  console.log(newArr);

  //clear send command box
  document.getElementById("div2").innerHTML =""

  //clear prev display on well
  document.getElementById("historywell").innerHTML =""

  //display previous movement on well
  for (let i=0; i < newArr.length; i++){
    document.getElementById("historywell").innerHTML += newArr[i] + "<br>"
  }

  //For applying duration on movements
  var delay = ( function() {
      var timer = 0;
      return function(callback, ms) {
          clearTimeout (timer);
          timer = setTimeout(callback, ms);
      };
  })();

  //Function for duration on movements
  function moveDuration(i){
    delay(function(){
            clearmove();// stop moving
        }, i ); // end delay

  }


  //Go through the array of "sent" commands
  for (let i=0; i < newArr.length; i++){

    //Forward movement + duration
    //If no duration sent, default is 1000ms
    if(newArr[i]=="Forward"){
      if(newArr[i+1]=="For 1 second"){
        moveleft();
        moveDuration(1000);
      }else if(newArr[i+1]=="For 2 seconds"){
        moveleft();
        moveDuration(2000);
      }else if(newArr[i+1]=="For 3 seconds"){
        moveleft();
        moveDuration(3000);
      }else{
        moveleft();
        moveDuration(1000);
      }

    //Turn right has to be followed by forward/reverse
    //for the car to move
    //If no duration sent, default is 1000ms
    }else if(newArr[i]=="Turn Right"){
      if(newArr[i+1]=="Forward"){
        if(newArr[i+2]=="For 1 second"){
          moveup();
          moveDuration(1000);
          newArr.splice(i+1, 1); //remove "Forward" element from array to prevent repetition
        }else if(newArr[i+2]=="For 2 seconds"){
          moveup();
          moveDuration(2000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 3 seconds"){
          moveup();
          moveDuration(3000);
          newArr.splice(i+1, 1); //remove "Forward" element from array to prevent repetition
        }else{
          moveup();
          moveDuration(1000);
          newArr.splice(i+1, 1); //remove "Forward" element from array to prevent repetition
        }
      }else if(newArr[i+1]=="Reverse"){
        if(newArr[i+2]=="For 1 second"){
          movedown();
          moveDuration(1000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 2 seconds"){
          movedown();
          moveDuration(2000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 3 seconds"){
          movedown();
          moveDuration(3000);
          newArr.splice(i+1, 1);
        }else{
          movedown();
          moveDuration(1000);
          newArr.splice(i+1, 1);
        }
      }

    //Turn Left has to be followed by forward/reverse
    //for the car to move
    //If no duration sent, default is 1000ms
    }else if(newArr[i]=="Turn Left"){
      if(newArr[i+1]=="Forward"){
        if(newArr[i+2]=="For 1 second"){
          movedown();
          moveDuration(1000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 2 seconds"){
          movedown();
          moveDuration(2000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 3 seconds"){
          movedown();
          moveDuration(3000);
          newArr.splice(i+1, 1);
        }else{
          movedown();
          moveDuration(1000);
          newArr.splice(i+1, 1);
        }
      }else if(newArr[i+1]=="Reverse"){
        if(newArr[i+2]=="For 1 second"){
          moveup();
          moveDuration(1000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 2 seconds"){
          moveup();
          moveDuration(2000);
          newArr.splice(i+1, 1);
        }else if(newArr[i+2]=="For 3 seconds"){
          moveup();
          moveDuration(3000);
          newArr.splice(i+1, 1);
        }else{
          moveup();
          moveDuration(1000);
          newArr.splice(i+1, 1);
        }
      }
    }else if(newArr[i]=="Reverse"){
      if(newArr[i+1]=="For 1 second"){
        moveright();
        moveDuration(1000);
      }else if(newArr[i+1]=="For 2 seconds"){
        moveright();
        moveDuration(2000);
      }else if(newArr[i+1]=="For 3 seconds"){
        moveright();
        moveDuration(3000);
      }else{
        moveright();
        moveDuration(1000);
      }

    }
  }


}

//HELLO AFIQ HEREHERE
//for validation of commands
//can edit here also
function readTextFile(file, student_input)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                if(String(student_input)==String(allText)){
                  alert("That's correct!! Car shall be moving now!");
                }else{
                  alert("Wrong answer! Try again!")
                }

            }
        }
    }
    rawFile.send(null);
}

//Drag and Drop commands
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}


function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  var isLeft = 'drag1' == data || "drag2" == data || "drag3" == data || "drag4" == data || "drag5" == data || "drag6" == data || "drag7" == data || "drag8" == data || "drag9" == data;
  var nodeCopy = document.getElementById(data).cloneNode(true);
  nodeCopy.id = "img" + ev.target.id;
  if (!isLeft) {
    sourceNode = document.getElementById(data);
    sourceNode.parentNode.removeChild(sourceNode);
  }
  ev.target.appendChild(nodeCopy);
  ev.stopPropagation();
  return false;
}

function dropNO(ev){
  //alert("please lah")
  drop(ev)
  //location.reload();
  var myobj = document.getElementById("imgimgdiv2");
  myobj.remove();
}