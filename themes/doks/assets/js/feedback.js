function handleFeedbackClick(element){
  var opposite = (element.dataset.action === 'like') ? 'opinion-dislike' : 'opinion-like';
  document.getElementById(opposite).classList.remove('show');

  ga('send', 'event', 'Feedback', element.dataset.action, element.dataset.doc);
}

export function feedbackDocs(){
  var div_feedback = document.getElementsByClassName('docs-feedback')[0];

  if (typeof div_feedback !== 'undefined'){
    if (typeof ga !== 'undefined') {
      div_feedback.classList.remove('d-none');

      var like = document.getElementById('like-doc-btn');
      var dislike = document.getElementById('dislike-doc-btn');

      like.addEventListener('click', function () {
        handleFeedbackClick(like);
      });

      dislike.addEventListener('click', function () {
        handleFeedbackClick(dislike);
      });
    }
    else{
      console.error('Google Analytic not load');
    }
  }
}
