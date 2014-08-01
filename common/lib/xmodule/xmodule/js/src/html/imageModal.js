$(document).on('load_xmodule', 'a.modal-content img', function () {
    'use strict';

    var body = $('body');
    var wrapper = replaceHtml(this);
    var imageWrapper = wrapper.find('.image-wrapper');
    var image = imageWrapper.find('img');
    var imageModal = wrapper.find('.image-modal');
    var imageLink = wrapper.find('.image-link');
    var imageContent = imageModal.find('.image-content');
    var imageControls = imageContent.find('.image-controls');
    var actionClose = imageContent.find('.action-close');
    var actionZoomIn = imageControls.find('.action-zoom-in');
    var actionZoomOut = imageControls.find('.action-zoom-out');
    var modalUiIcon = imageControls.find('.modal-ui-icon');
    var draggie = new Draggabilly(image[0], {
        containment: true
    });

    function attachEvents() {
        draggie.disable();
        imageLink.click(openModal);
        imageModal.click(hideModal);
        actionClose.click(hideModal);
        image.click(preventEventBubbling);
        imageControls.click(preventEventBubbling);
        actionZoomOut.click(toggleZoom);
        actionZoomIn.click(toggleZoom);
    }
    function preventEventBubbling() {
        return false;
    }
    function openModal() {
        imageModal.addClass('image-is-fit-to-screen');
        body.css('overflow', 'hidden');
        return false;
    }
    function hideModal() {
        imageModal
            .removeClass('image-is-fit-to-screen')
            .removeClass('image-is-zoomed')
        ;
        actionZoomIn.removeClass('is-disabled');
        actionZoomOut.addClass('is-disabled');
        draggie.disable();
        body.css('overflow', 'auto');
        return false;
    }
    function toggleZoom(event) {
        if (!$(event.target).parent().hasClass('is-disabled')) {
            modalUiIcon.toggleClass('is-disabled');
            imageModal
                .toggleClass('image-is-fit-to-screen')
                .toggleClass('image-is-zoomed')
            ;
            if (draggie.isEnabled) {
                draggie.disable();
            } else {
                draggie.enable();
                centerImage();
            }
        }
        return false;
    }
    function centerImage() {
        var imgWidth = image.width();
        var imgHeight = image.height();
        var imgContainerOffsetLeft = imgWidth - imageContent.width();
        var imgContainerOffsetTop = imgHeight - imageContent.height();
        var imgContainerWidth = imgWidth + imgContainerOffsetLeft;
        var imgContainerHeight = imgHeight + imgContainerOffsetTop;
        image.css({
            top: imgContainerOffsetTop / 2,
            left: imgContainerOffsetLeft / 2
        });
        imageWrapper.css({
            top: -imgContainerOffsetTop,
            left: -imgContainerOffsetLeft,
            width: imgContainerWidth,
            height: imgContainerHeight
        });
    }
    function replaceHtml(that) {
        var data;
        var html;
        var image = $(that);
        var image_alt = image.attr('alt');
        var anchor = image.parent();
        var anchor_href = anchor.attr('href');
        var anchor_html = anchor.html();
        var template = $('#image-modal-tpl');
        if (!anchor_href) {
            return;
        }
        data = {
            "smallHtml": anchor_html,
            "largeAlt": image_alt,
            "largeSrc": anchor_href
        };
        html = _.template(template.text(), data);
        wrapper = $(html);
        anchor.replaceWith(wrapper);
        return wrapper;
    }

    attachEvents();
});

