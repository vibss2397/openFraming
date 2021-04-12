
/* * * * * */
/*  DATA   */
/* * * * * */


function getTMPreview(id) {
    const GET_ONE_TOPIC_MDL = BASE_URL + `/topic_models/${id}/topics/preview`;
    $.ajax({
        url: GET_ONE_TOPIC_MDL,
        type: "GET",
        dataType: "json",
        success: function (data) {
            $('#tm-prev-name').empty().append(data.topic_model_name);
            $('#tm-prev-num').empty().append(data.num_topics);
            $('#previews').empty();
            for (let i = 0; i < data.topic_previews.length; i++) {
                formatPreviews(data.topic_names[i], data.topic_previews[i]);
            }
        },
        error: function (xhr, status, err) {

        },
    });
}

/* * * * * * */
/*  BROWSER  */
/* * * * * * */
$(document).ready(function() {
    const id = urlParams.get('id');

    if (id !== null) {
        // getTMPreview(id);

        let data = {
            topic_model_name: 'model1',
            num_topics: 2,
            topic_names: ['Topic 1', 'Topic 2'],
            topic_previews: [
                {
                    keywords: ['one', 'two', 'three'],
                    examples: ['test1', 'test2', 'test3']
                },
                {
                    keywords: ['one', 'two', 'three'],
                    examples: ['test1', 'test2', 'test3']
                },
            ]
        };
        $('#tm-prev-name').empty().append(data.topic_model_name);
        $('#tm-prev-num').empty().append(data.num_topics);
        $('#previews').empty();
        for (let i = 0; i < data.topic_previews.length; i++) {
            formatPreviews(data.topic_names[i], data.topic_previews[i]);
        }


    }


});


/* * * * * * * */
/*  HELPERS    */
/* * * * * * * */


function formatPreviews(name, preview) {
    let keywords = formatLists(preview.keywords);
    let examples = formatLists(preview.examples);
    let newDiv = `
              <div>
                <div class="row">
                  <div class="col-4">Topic Name</div>
                  <div class="col">${name}</div>
                </div>
                <div class="row">
                  <div class="col-4">Keywords</div>
                  <div class="col">
                    ${keywords}
                  </div>
                </div>
                <div class="row">
                  <div class="col-4">Examples</div>
                  <div class="col">
                    ${examples}
                  </div>
                </div>
                <hr>
              </div>
    `;
    $('#previews').append(newDiv);
}


function formatLists(list) {
    let newList = `<ul>\n`;
    for (let item of list) {
        newList += `<li>${item}</li>\n`;
    }
    newList += '</ul>';
    return newList;

}









