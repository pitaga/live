
var canvas = document.getElementById('canvas');
var cvs = canvas.getContext('2d');  
var drawing =false;
var penWeight = 0;      //画笔粗细  
var penColor = '';  //画笔颜色 
var filling =false;
cvs.history = [];
cvs.strokeStyle = penColor;     //画笔颜色  
cvs.lineWidth = penWeight;      //画笔粗细

window.onload = function(){
	canvas.onmousedown = function(e){
		/*找到鼠标（画笔）的坐标*/
		var start_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;
		var start_y = e.clientY - canvas.offsetTop + document.body.scrollTop;
		cvs.beginPath();    //开始本次绘画
		cvs.moveTo(start_x, start_y);   //画笔起始点
		/*设置画笔属性*/
		cvs.lineCap = 'round';
		cvs.lineJoin ="round";
		canvas.onmousemove = function(e){
			/*找到鼠标（画笔）的坐标*/
			var move_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;
			var move_y = e.clientY - canvas.offsetTop + document.body.scrollTop;
			cvs.lineTo(move_x, move_y);     //根据鼠标路径绘画
			cvs.stroke();   //立即渲染
        }
		canvas.onmouseup = function(e){
			cvs.history.push(cvs.getImageData(0,0,canvas.width,canvas.height));
			cvs.closePath();    //结束本次绘画
			canvas.onmousemove = null;  // 清空鼠标移动事件
			canvas.onmouseup = null;  // 清空鼠标移出事件
        }
        canvas.onmouseleave = function(){
            cvs.closePath();
            canvas.onmousemove = null;
            canvas.onmouseup = null;
        }
	}
}

function paint(){
	canceleraser();
	canvas.onmousedown = function(e){ 
		/*找到鼠标（画笔）的坐标*/  
		var start_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;  
		var start_y = e.clientY - canvas.offsetTop + document.body.scrollTop;  
		cvs.beginPath();    //开始本次绘画  
		cvs.moveTo(start_x, start_y);   //画笔起始点  
		/*设置画笔属性*/  
		cvs.lineCap = 'round';  
		cvs.lineJoin ="round"; 		
		canvas.onmousemove = function(e){
			/*找到鼠标（画笔）的坐标*/  
			var move_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;  
			var move_y = e.clientY - canvas.offsetTop + document.body.scrollTop;   
			cvs.lineTo(move_x, move_y);     //根据鼠标路径绘画  
			cvs.stroke();   //立即渲染  
        }
		canvas.onmouseup = function(e){
			cvs.history.push(cvs.getImageData(0,0,canvas.width,canvas.height));
			cvs.closePath();    //结束本次绘画
			canvas.onmousemove = null;  // 清空鼠标移动事件
			canvas.onmouseup = null;  // 清空鼠标移出事件
        }  
        canvas.onmouseleave = function(){
            cvs.closePath();
            canvas.onmousemove = null;  
            canvas.onmouseup = null; 
        }
	}
}

function figure(figtype){
	canceleraser();
	if (figtype == "none")
	{
		paint();
		return;
	}
	canvas.onmousedown = function(e){ 
		/*找到鼠标（画笔）的坐标*/  
		var start_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;  
		var start_y = e.clientY - canvas.offsetTop + document.body.scrollTop;
		x2 = start_x;
		y2 = start_y;
		var temp = cvs.getImageData(0,0,canvas.width,canvas.height)

		canvas.onmousemove = function(e){
			cvs.putImageData(temp, 0, 0);
			cvs.beginPath();    //开始本次绘画 
			/*找到鼠标（画笔）的坐标*/  
			var move_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;  
			var move_y = e.clientY - canvas.offsetTop + document.body.scrollTop;   
			x1 = move_x;
			y1 = move_y;
			endt_x = move_x;
			endt_y = move_y;
			if (figtype == "line")
			{
				cvs.moveTo(x1 - 0.5,y1 - 0.5);
				cvs.lineTo(x2 - 0.5,y2 - 0.5);
				if (filling){
					cvs.stroke();
				}
			}
			else if (figtype == "rect")
			{
				cvs.rect(endt_x - 0.5, endt_y - 0.5, start_x-endt_x, start_y-endt_y);
			}
			else if (figtype == "triangle")
			{
				cvs.moveTo(start_x, start_y);
				cvs.lineTo(endt_x,endt_y);
				cvs.lineTo(start_x,endt_y);
				cvs.lineTo(start_x,start_y);
			}
			else if (figtype == "circle")
			{
				var r= Math.sqrt(Math.pow(x2-endt_x,2),Math.pow(y2-endt_y),2);
				cvs.arc(endt_x,endt_y,r,0,2*Math.PI);
			}
			else if (figtype == "ellipse")
			{
				for(var i=0;i<2*Math.PI;i+=0.01){
					cvs.lineTo(((x2-x1)/2)*Math.cos(i)+(x2+x1)/2,((y2-y1)/2)*Math.sin(i)+(y2+y1)/2);
				}
			}
			else
			{
				return;
			}
			
			if (filling){
				cvs.fillStyle=cvs.strokeStyle;
				cvs.fill();
			}
			else{
				cvs.stroke();
			}
			cvs.closePath();    //结束本次绘画			
		}
		canvas.onmouseup = function(e){
			cvs.putImageData(temp, 0, 0);
			cvs.beginPath();    //开始本次绘画 
			var endt_x = e.clientX - canvas.offsetLeft + document.body.scrollLeft;  
			var endt_y = e.clientY - canvas.offsetTop + document.body.scrollTop; 
			x1 = endt_x;
			y1 = endt_y;
			if (figtype == "line")
			{
				cvs.moveTo(x1 - 0.5,y1 - 0.5);
				cvs.lineTo(x2 - 0.5,y2 - 0.5);
				if (filling){
					cvs.stroke();
				}
			}
			else if (figtype == "rect")
			{
				cvs.rect(endt_x - 0.5, endt_y - 0.5, start_x-endt_x, start_y-endt_y);
			}
			else if (figtype == "triangle")
			{
				cvs.moveTo(start_x, start_y);
				cvs.lineTo(endt_x,endt_y);
				cvs.lineTo(start_x,endt_y);
				cvs.lineTo(start_x,start_y);
			}
			else if (figtype == "circle")
			{
				var r= Math.sqrt(Math.pow(x2-endt_x,2),Math.pow(y2-endt_y),2);
				cvs.arc(endt_x,endt_y,r,0,2*Math.PI);
			}
			else if (figtype == "ellipse")
			{
				for(var i=0;i<2*Math.PI;i+=0.01){
					cvs.lineTo(((x2-x1)/2)*Math.cos(i)+(x2+x1)/2,((y2-y1)/2)*Math.sin(i)+(y2+y1)/2);
				}
			}
			else
			{
				return;
			}
			
			if (filling){
				cvs.fillStyle=cvs.strokeStyle;
				cvs.fill();
			}
			else{
				cvs.stroke();
			}		
			cvs.closePath();    //结束本次绘画
			cvs.history.push(cvs.getImageData(0,0,canvas.width,canvas.height));
			canvas.onmousemove = null;  // 清空鼠标移动事件
			canvas.onmouseup = null;  // 清空鼠标移出事件
        }  
        canvas.onmouseleave = function(){
            cvs.closePath();
            canvas.onmousemove = null;  
            canvas.onmouseup = null; 
        }
	}
}

//撤销
function backstep(){
	canceleraser();
	if (cvs.history.length == 0) {
		alert("无效操作");
		return;
	}
	cvs.clearRect(0, 0, canvas.width, canvas.height);
	cvs.history.pop();
	cvs.putImageData(cvs.history[cvs.history.length - 1], 0, 0);
}

//选中橡皮擦
function checkeraser(){
	document.getElementById("eraser").value = "正在使用...";
	cvs.globalCompositeOperation = "destination-out";
	function getBoundingClientRect(x,y){
		var box = canvas.getBoundingClientRect(); //获取canvas的距离浏览器视窗的上下左右距离
		return {x:x-box.left,
				y:y-box.top
		}
	}
	canvas.onmousedown = function(e){
		var first = getBoundingClientRect(e.clientX,e.clientY);
		cvs.save();
		cvs.beginPath();
		cvs.moveTo(first.x,first.y);
		drawing = true;
	}
	canvas.onmousemove = function(e){
		if(drawing){
			var move = getBoundingClientRect(e.clientX,e.clientY);
			cvs.save();
			cvs.lineTo(move.x,move.y);
			cvs.stroke()
			cvs.restore()
		}
	}
	canvas.onmouseup = function(){
		cvs.history.push(cvs.getImageData(0,0,canvas.width,canvas.height));
		drawing = false;
	}
	canvas.onmouseleave = function(){
		drawing = false;
		canvas.onmouseup();
	}
}

//隐藏提示
function hidenotice(){
	document.getElementById("notice").style.display="none";
}

//取消橡皮擦
function canceleraser(){
	document.getElementById("eraser").value = "橡皮擦";
    cvs.globalCompositeOperation = "source-over";
}

//设置填充
function fill(){
	canceleraser();
	var chk = document.getElementById("filling").checked;
	if (chk){
		filling = true;
	}
	else{
		filling =false;
	}
}

function checkpen(width){ //设置笔的粗细
    cvs.lineWidth = width;
}

function changecolor(pencolor){ //设置颜色
	cvs.strokeStyle =pencolor;
}

function clearcanvas(){ //清空画板
	canceleraser();
    cvs.clearRect(0,0,canvas.width,canvas.height);
}
