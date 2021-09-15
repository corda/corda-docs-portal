import hljs from 'highlight.js/lib/core';

import javascript from 'highlight.js/lib/languages/javascript';
import json from 'highlight.js/lib/languages/json';
import bash from 'highlight.js/lib/languages/bash';
import handlebars from 'highlight.js/lib/languages/handlebars';
import ini from 'highlight.js/lib/languages/ini';
import yaml from 'highlight.js/lib/languages/yaml';
import markdown from 'highlight.js/lib/languages/markdown';
import kotlin from 'highlight.js/lib/languages/kotlin';
import java from 'highlight.js/lib/languages/java';
import groovy from 'highlight.js/lib/languages/groovy';
import gradle from 'highlight.js/lib/languages/gradle';
import shell from 'highlight.js/lib/languages/shell';
import gauss from 'highlight.js/lib/languages/gauss';
import docker from 'highlight.js/lib/languages/dockerfile';
import sql from 'highlight.js/lib/languages/sql';

hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('json', json);
hljs.registerLanguage('bash', bash);
hljs.registerLanguage('html', handlebars);
hljs.registerLanguage('ini', ini);
hljs.registerLanguage('toml', ini);
hljs.registerLanguage('yaml', yaml);
hljs.registerLanguage('md', markdown);
hljs.registerLanguage('kotlin', kotlin);
hljs.registerLanguage('java', java);
hljs.registerLanguage('groovy', groovy);
hljs.registerLanguage('gradle', gradle);
hljs.registerLanguage('shell', shell);
hljs.registerLanguage('gauss', gauss);
hljs.registerLanguage('docker', docker);
hljs.registerLanguage('sql', sql);

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('pre code').forEach((element) => {
    if (element.classList.contains('language-none') || element.classList.length === 0){
      element.classList.add('hljs');
      var parent = element.parentElement.parentElement;
      var div = document.createElement('div');
      div.classList.add('highlight');

      var pre = element.parentElement;
      parent.insertBefore(div, pre.nextSibling);

      div.append(pre);
    }
  });

  document.querySelectorAll('.highlight').forEach((parent) => {
    var blocks = parent.getElementsByTagName('code');
    if (blocks.length > 0) {
      var block = blocks[0];
      hljs.highlightElement(block);

      var divButton = document.createElement('div');
      divButton.classList.add('copy-code');

      var button = document.createElement('button');
      button.innerText = 'Copy';
      button.onclick = function () {
        CopyCode(block, button);
      };

      divButton.append(button);

      parent.prepend(divButton);
    }
  });

  document.querySelectorAll('.highlight span').forEach((span) => {
    if (span.style.color == 'rgb(0, 0, 0)'){
      span.style.color = '#fff';
    }
    else if (span.style.color == 'rgb(0, 0, 207)' || span.style.color == 'rgb(32, 74, 135)'){
      span.style.color = '#3593E7';
    }
  });
});

function CopyCode(code, button) {
  console.log(code);
  if (code.tagName.toLowerCase() === 'code') {
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

    button.innerText = 'Copied';

    setTimeout(function () {
      button.innerText = 'Copy';
    }, 5000, button);
  }
}
