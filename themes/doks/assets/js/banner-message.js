const timeoutDuration = 5000 //milliseconds
const $bannerMessagesContainer = document.querySelector('[data-banner-messages-container]')
const numberOfMessages = $bannerMessagesContainer.children.length
$bannerMessagesContainer.children[0].classList.add("banner-message__item--active")

if (numberOfMessages > 0) {
  if (window.location.pathname == "/") {
    let currentMessage = 0;
    setInterval(() => {
      let nextMessage = (currentMessage === numberOfMessages - 1) ? 0 : currentMessage + 1
      $bannerMessagesContainer.children[currentMessage].classList.remove("banner-message__item--active")
      $bannerMessagesContainer.children[nextMessage].classList.add("banner-message__item--active")
      currentMessage = nextMessage
    }, timeoutDuration)
  }
}
