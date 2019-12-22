async function vote(post_id, up) {
  data = await fetch("/vote", {
    method: "POST",
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      post_id: post_id,
      up: up
    })
  });

  json = await data.json();
  return json;
}

async function vote_event(post_id, btn, up) {
  var json;
  try {
    json = await vote(post_id, up);
  } catch (err) {
  }

  if (json) {
    btn.style.color = up ? "green" : "red";
  }
}

function setup() {
  let cards = document.getElementsByClassName("feed_card");
  console.log(cards);
  for (let i=0; i<cards.length; i++) {
    let post_id = parseInt(cards[i].getAttribute("post_id"), 10);
    let up_button = cards[i].getElementsByClassName("upvote")[0];
    up_button.addEventListener("click", function() {
      vote_event(post_id, up_button, true);
    });
    let down_button = cards[i].getElementsByClassName("downvote")[0];
    down_button.addEventListener("click", function() {
      vote_event(post_id, down_button, false);
    });
  }
}

setup();
