$(document).ready(function() {
  $('button.like').click(function() {
      var $obj = $(this);
      var target_id = $obj.attr('id').split('_')[1];
      $obj.prop('disabled', true);
      $.ajax({
      url: '/like/add-or-remove',
      type: 'POST',
      data: {target_model: $obj.attr('model'),
             target_object_id: target_id},
      success: function(response) {
        var status = response.split("|")[0];
        var count = response.split("|")[1];
          if (status == 'added') {
            $(".like-" + target_id).removeClass('fa-heart-o').addClass('fa-heart');
          }
          else {
            $(".like-" + target_id).removeClass('fa-heart').addClass('fa-heart-o');
          }
          $(".like-count-" + target_id).html(count);
          $obj.prop('disabled', false);
      }
      });
  });
});