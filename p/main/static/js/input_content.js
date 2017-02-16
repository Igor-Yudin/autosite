
// This function bound buttons add paragraph and remove paragraph with
// click event.
function bound_buttons(){
  	$('.add-btn').each(function() {
	  	$(this).on('click', function() {

		  	var target = $(this).attr('target');

		  	var total_id = '#id_' + target + '_p-TOTAL_FORMS';
		  	var empty_id = '#empty_' + target;
		  	var formset_id = '#id_' + target + '_p_formset';

		  	var form_idx = $(total_id).val();

		  	// Append empty form to the formset
		  	// and increment the TOTAL_FORMS value
		  	//
		  	// Get div with id=empty_name, take inner html
		  	// from it and replace all __prefix__ stubs
		  	// (they are made by django)
		  	$(formset_id).append($(empty_id).html().replace(/__prefix__/g, form_idx));
		  	$(total_id).val(parseInt(form_idx) + 1);
			})
		});

	$('.rmv-btn').each(function() {
	  	$(this).on('click', function() {

		  	var target = $(this).attr('target');

		  	var total_id = '#id_' + target + '_p-TOTAL_FORMS';
		  	var formset_id = '#id_' + target + '_p_formset';

		  	var form_idx = $(total_id).val();
		  	if (form_idx == 0)
		  		return;

		  	// Remove the last div element, which is wrapper for
		  	// last form and decrement the TOTAL_FORMS value
		  	$(formset_id + '> div').last().remove();
		  	$(total_id).val(parseInt(form_idx) - 1);
		})
	});
}

function unbound_buttons() {
	$('.add-btn').each(function() {
		$(this).off('click');
	});

	$('.rmv-btn').each(function() {
		$(this).off('click');
	});
}


// This function bounds checkboxes, so
// when checkbox changes its state:
// to uncheked:
//   page div block with id=chb_name + '_page'
//   is cut and saved in buffer and the hidden input
//   with name 'order' changes its value to the
//   current order of pages
//
// to checked:
//   page with name as selected checkbox is taken from buffer
//   and then inserted in the end of page div-block.
//   It also bounds all buttons 'add paragraph' and 'remove paragraph',
//   as inserted buttons aren't bounded.
//   And it also change order value, appending to it name of inserted page.
//
// Get dictionary buffer with deleted pages.
// *all checkboxes are checked at start and
// *the order is set correctly from view
function bound_checkboxes(buffer) {
	$(':checkbox').each(function() {
	  	$(this).change(function() {
	  		var checked = $(this).prop('checked');
	  		var name = $(this).attr('name');
  			var page_id = "#" + name + "_page";
  			var order_id = '#order';

	  		if (checked)
	  		{
	  			 $('#pages').append(buffer[name]);

	  			 // Before bound buttons, it we should unbound all.
	  			 // Otherwise those buttons we append now would be
	  			 // bouned once, and others would be bounded one more time.
	  			 unbound_buttons();
	  			 bound_buttons();

	  			 var order = $(order_id).val();

	  			 if (order != "")
	  			 {
	  			 	order = order.split(',');
	  			 }
	  			 else
	  			 	order = [];

	  			 order.push(name);
	  			 $(order_id).val(order.join());
	  		}
	  		else
	  		{
	  			// html() method returns only inner html, while
	  			// there should be html-code, like:
	  			//
	  			// <div id="name_page">
	  			//   <inner_html>
	  			// </div>
	  			//
	  			// So it wraps inner html to the div-wrapper
	  			// It might be done simplier with format(), [than with regex]
	  			// but there's no such method.
	  			buffer[name] = $(page_id).clone(); // '<div id="{0}_page">{1}</div>'.replace('{0}', name).replace('{1}', $(page_id).html());
	  			$(page_id).remove();

	  			var order = $(order_id).val().split(',');
	  			var ind = order.indexOf(name);
	  			if (ind > -1)
	  			  order.splice(ind, 1);
	  			$(order_id).val(order.join());
	  		}
	  	})
    });
}