import hljs from 'highlight.js/lib/core';

import javascript from 'highlight.js/lib/languages/javascript';
import json from 'highlight.js/lib/languages/json';
import bash from 'highlight.js/lib/languages/bash';
import htmlbars from 'highlight.js/lib/languages/htmlbars';
import ini from 'highlight.js/lib/languages/ini';
import yaml from 'highlight.js/lib/languages/yaml';
import markdown from 'highlight.js/lib/languages/markdown';
import kotlin from 'highlight.js/lib/languages/kotlin';
import java from 'highlight.js/lib/languages/java';

hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('json', json);
hljs.registerLanguage('bash', bash);
hljs.registerLanguage('html', htmlbars);
hljs.registerLanguage('ini', ini);
hljs.registerLanguage('toml', ini);
hljs.registerLanguage('yaml', yaml);
hljs.registerLanguage('md', markdown);
hljs.registerLanguage('kotlin', kotlin);
hljs.registerLanguage('java', java);

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('pre code').forEach((block) => {
    hljs.highlightElement(block);

    let parent = block.parentElement.parentElement;

    if (parent.classList.contains('tab-pane')) {
      var divButton = document.createElement('div');
      divButton.classList.add('copy-code');

      var button = document.createElement('button');
      button.innerText = 'Copy';
      button.onclick = function () {
        CopyCode(this.parentElement);
      };

      divButton.append(button);

      parent.prepend(divButton);
    }
  });

  document.querySelectorAll('.highlight span').forEach((span) => {
    if (span.style.color == 'rgb(0, 0, 0)'){
      span.style.color = '#fff';
    }
  });
});

function CopyCode(element){
  var success = false;
  var pre = element.nextElementSibling;
  if (pre.tagName.toLowerCase() === 'pre'){
    var code = pre.childNodes[0];
    if (code.tagName.toLowerCase() === 'code'){
      var text = code.textContent || code.innerText;

      // Create a textblock and assign the text and add to document
      var el = document.createElement('textarea');
      el.value = text.trim();
      document.body.appendChild(el);
      el.style.display = 'block';

      // select the entire textblock
      if (window.document.documentMode)
        el.setSelectionRange(0, el.value.length);
      else
        el.select();

      // copy to clipboard
      document.execCommand('copy');

      // clean up element
      document.body.removeChild(el);

      element.childNodes[0].innerText = 'Copied';

      setTimeout(function(){
        element.childNodes[0].innerText = 'Copy';
      }, 5000, element);
      success = true;
    }
  }

  if (success === false){
    element.childNodes[0].innerText = 'Error';
  }
}
