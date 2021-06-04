/* * * * * * */
/*  BROWSER  */
/* * * * * * */
$(document).ready(function() {
    const id = urlParams.get('id');


    $('#pt-testing-visible').on('click', function () {
        $('#pt-testing-invisible').click();
    });

    $("input[id='pt-testing-invisible']").change(function() {
        let file = $(this).val().split('\\').pop();
        $('#pt-testing-filepath')
            .html(`File chosen: ${file}`)
            .removeClass('hidden');
    });


    $('#submit5').on('click', function () {
        // handle missing info first
        if (($("input[name='policyissue']:checked").length === 0) && ($('#pt-id').val() === "")) {
            $('#error5-text').html('Please select a pretrained classifier.');
            $('#error5').removeClass('hidden');
        } else if (($("input[name='policyissue']:checked").length > 0) && ($('#pt-id').val() !== "")) {
            $('#error5-text').html('You have selected one of our classifiers and provided your own ID. Please clear one of these fields and try again.');
            $('#error5').removeClass('hidden');
        } else if (document.getElementById("pt-testing-invisible").files.length === 0) {
            $('#error5-text').html('Please provide a test file.');
            $('#error5').removeClass('hidden');
        } else if ($('#pt-name').val() === "") {
            $('#error5-text').html('Please name your test set.');
            $('#error5').removeClass('hidden');
        } else if ($('#pt-email').val() === "") {
            $('#error5-text').html('Please provide an email address.');
            $('#error5').removeClass('hidden');
        } else {

            $('#error5').addClass('hidden');

            let id;
            if ($('#pt-id').val() === "") {
                id = $("input[name='policyissue']:checked").val()
            } else {
                id = $('#pt-id').val()
            }
            console.log(id);
            // POST request for topic model
            const POST_TEST_SET = `${BASE_URL}/classifiers/${id}/test_sets/`;
            let postData = {
                test_set_name: $('#pt-name').val(),
                notify_at_email: $('#pt-email').val()
            };
            $.ajax({
                url: POST_TEST_SET,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(postData),
                success: function (data) {
                    console.log('success in classifier test set POST');
                    // POST request for training file
                    const POST_PT_TESTING_FILE = `${BASE_URL}/classifiers/${data.classifier_id}/test_sets/${data.test_set_id}/file`;
                    let fileFD = new FormData();
                    fileFD.append('file', document.getElementById("pt-testing-invisible").files[0]);

                    $.ajax({
                        url: POST_PT_TESTING_FILE,
                        data: fileFD,
                        type: 'POST',
                        processData: false,
                        contentType: false,
                        success: function(){
                            console.log('STEP 5 - success in testing file POST');
                            $('#success5').removeClass('hidden');
                        },
                        error: function (xhr, status, err) {
                            console.log(xhr.responseText);
                            let error = getErrorMessage(JSON.parse(xhr.responseText).message);
                            $('#error5').html(`An error occurred while uploading your file: ${error}`).removeClass('hidden');
                        }
                    });
                },
                error: function (xhr, status, err) {
                    console.log(xhr.responseText);
                    let error = getErrorMessage(JSON.parse(xhr.responseText).message);
                    $('#error5').html(`An error occurred while creating the test set: ${error}`).removeClass('hidden');
                }
            });
        }
    });

});


/* * * * * * * */
/*  HELPERS    */
/* * * * * * * */


function clearOptions() {
    $("input[name='policyissue']:checked").val([]);
}





















