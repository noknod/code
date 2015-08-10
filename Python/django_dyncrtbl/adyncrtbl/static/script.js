//var canvas, ctx;
//var width = 300, height = 300;
//var x = 50, y = 350;

var types = {0 : 'IntegerField', 1 : 'CharField', 2 : 'TextField'};
var indexes = []
var max_index = -1
var submitButton = null;

//var incX = 3;
//var size = 20;
//var currentColor= 'red';

function init() {
    var fields = document.getElementById('fields');
 
    submitButton = document.getElementsByClassName('submitDo')[0];
    submitButton.disabled = true;
    //button.addEventListener("click", submit(event));
}


function remove(id) {
    return (elem=document.getElementById(id)).parentNode.removeChild(elem);
}


function removeField(index) {
    var id = 'field' + index;
    var fieldset = document.getElementById(id);
    var name = fieldset.getElementsByClassName('columnname')[0].value;
    if (confirm('Удалить поле ' + name + '?')) {
        remove(id);
        indexes.splice(indexes.indexOf(index), 1);
        document.getElementsByClassName('submitDo')[0].disabled = (indexes.length === 0);
    }
}


function createField(type) {
    if (confirm('Добавить поле ' + types[type] + '?')) {
        max_index += 1;

        var fieldset = document.createElement('fieldset');
        fieldset.setAttribute('class', 'field');
        fieldset.setAttribute('id', 'field' + max_index);
        fieldset.appendChild(document
            .createElement('legend'))
            .textContent = types[type];

        var div = document.createElement('div');
        var label = document.createElement('label');
        label.setAttribute('for', 'columnname' + max_index);
        label.textContent = 'Название столбца';
        div.appendChild(label);
        var input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('class', 'columnname');
        input.setAttribute('id', 'columnname' + max_index);
        input.setAttribute('pattern', '^[a-zA-Z]+$');
        input.setAttribute('placeholder', 'Только латинские буквы');
        input.setAttribute('required', '');
        input.setAttribute('name', 'name' + max_index);

        div.appendChild(input);
        fieldset.appendChild(div);

        if (types[type] === 'CharField') {
            var div = document.createElement('div');
            var label = document.createElement('label');
            label.setAttribute('for', 'length' + max_index);
            label.textContent = 'Длина';
            div.appendChild(label);
            var input = document.createElement('input');
            input.setAttribute('type', 'number');
            input.setAttribute('class', 'length');
            input.setAttribute('id', 'length' + max_index);
            input.setAttribute('value', '100');
            input.setAttribute('min', '1');
            input.setAttribute('required', '');
            input.setAttribute('name', 'length' + max_index);
            div.appendChild(input);
            fieldset.appendChild(div);
        }

        div = document.createElement('div');
        input = document.createElement('input');
        input.setAttribute('hidden', '');
        input.setAttribute('type', 'number');
        input.setAttribute('class', 'type');
        input.setAttribute('id', 'type' + max_index);
        input.setAttribute('value', type);
        input.setAttribute('min', '0');
        input.setAttribute('max', '2');
        input.setAttribute('name', 'type' + max_index);
        div.appendChild(input);
        fieldset.appendChild(div);

        div = document.createElement('div');
        input = document.createElement('input');
        input.setAttribute('type', 'button');
        input.setAttribute('class', 'remove');
        input.setAttribute('id', 'type' + max_index);
        input.setAttribute('value', 'Удалить столбец');
        input.setAttribute('onclick', 'removeField(' + max_index + ');');
        div.appendChild(input);
        fieldset.appendChild(div);

        fields.appendChild(fieldset);
        indexes[indexes.length] = max_index;
        submitButton.disabled = false;
    }
}


function submitDo() {
    var table_name = document.getElementById('name').value;
    if (confirm('Создать таблицу ' + table_name + '?')) {
        var csrftoken = getCookie('csrftoken');
        var form = document.forms[0];
        hide();
        var parameters = 'table=' + table_name;
        var fieldsets = form.getElementsByClassName('field');
        for (var i = 0; i < fieldsets.length; i++) {
            var name = fieldsets[i].getElementsByClassName('columnname')[0].value;
            var type = fieldsets[i].getElementsByClassName('type')[0].value;
            if (types[type] === 'CharField') {
                var length = fieldsets[i].getElementsByClassName('length')[0].value;
            }
            else var length = 0;
            var parameter = name + ',' + type + ',' + length;
            parameters += '&' + i + '=' + parameter;
        }
        var xmlhttp = getXmlHttp()
        xmlhttp.open("POST", '/dyncrtbl/create/', true);
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState != 4) return
                clearTimeout(timeout) // очистить таймаут при наступлении readyState 4
                if (xmlhttp.status == 200) {
                    alert('Таблица создана!\n\n' + xmlhttp.responseText);
                    location =  '/dyncrtbl/';
                } else {
                    handleError(xmlhttp.statusText + '\n\n' + xmlhttp.responseText)
                }
        };
        try {
            xmlhttp.send(parameters);
        }
        catch(error) {
            alert(error.name);
            show();
        }
        // Таймаут 10 секунд
        var timeout = setTimeout( function(){ xmlhttp.abort(); handleError("Time over") }, 10000);

       function handleError(message) {
            // обработчик ошибки
            alert('Ошибка: ' + message)
            show();
        }
    }
    return false;
}


function getXmlHttp(){
  var xmlhttp;
  try {
    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
  }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
  return xmlhttp;
}


function hide() {
    document.getElementsByClassName('main')[0].setAttribute('hidden', '');
    document.getElementsByClassName('wait')[0].removeAttribute('hidden');
}

function show() {
    document.getElementsByClassName('main')[0].removeAttribute('hidden');
    document.getElementsByClassName('wait')[0].setAttribute('hidden', '');
}



// csrf for Django
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
