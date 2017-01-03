$(function() {
  function stripeResponseHandler(status, response) {
    var $form = $('#payment-form');
    if (response.error) {
      $form.find('.payment-errors').text(response.error.message);
      $form.find('.submit').prop('disabled', false);
    } else {
      var token = response.id;
      $form.append($('<input type="hidden" name="stripe_token">').val(token));
      $form.get(0).submit();
    }
  };

  var $form = $('#payment-form');
  $form.submit(function(event) {
    $form.find('.submit').prop('disabled', true);

    Stripe.card.createToken($form, stripeResponseHandler);
    return false;
  });

  $('a.subscription').click(function (event) {
    event.preventDefault();
    $('.modal').fadeIn();
  });
  $('.modal').click(function (e) { if (e.target == $('.modal')[0]) $('.modal').fadeOut(); });
});
