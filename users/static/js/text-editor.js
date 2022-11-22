
const elements = document.querySelectorAll('.btn');
elements.forEach(element => {
element.addEventListener('click', () => {
let command = element.dataset['element'];
document.execCommand(command,false,null);
});
});

const textarea = document.querySelector('#content');

function f1(e){
let value = e.value;
textarea.style.fontSize = value + "px";
}

function downloadFile(filename, content) {
  const element = document.createElement('a');
  const blob = new Blob([content], { type: 'plain/text' });

  const fileUrl = URL.createObjectURL(blob);

  element.setAttribute('href', fileUrl);
  element.setAttribute('download', filename);
  element.style.display = 'none';

  document.body.appendChild(element);
  element.click();

  document.body.removeChild(element);
};

window.onload = () => {
  document.getElementById('download').
  addEventListener('click', e => {

    const filename = document.getElementById('filename').value;

    const content = document.querySelector('#content').innerHTML;

    if (filename && content) {
      downloadFile(filename, content);
    }
  });
};