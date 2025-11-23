document.addEventListener("DOMContentLoaded", function () {
    renderMathInElement(document.body, {
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "\\[", right: "\\]", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false },
        ],
    });
    $("input[name=radio_mode], .add_transformation, .remove_transformation").on("change", function() {
        const button_value = $("input[type='radio'][name='radio_mode']:checked").val();
        if (button_value === "discrete" && $(".input-p")) {
            $(".wrapper").css("max-width", "20em");
            $(".input-p").css("display", "none");
        } else if (button_value === "continuous" && $(".input-p")) {
            $(".wrapper").css("max-width", "25em");
            $(".input-p").css("display", "block");

        }
    });
});
window.WebFontConfig = {
    custom: {
        families: [
            "KaTeX_AMS",
            "KaTeX_Caligraphic:n4,n7",
            "KaTeX_Fraktur:n4,n7",
            "KaTeX_Main:n4,n7,i4,i7",
            "KaTeX_Math:i4,i7",
            "KaTeX_Script",
            "KaTeX_SansSerif:n4,n7,i4",
            "KaTeX_Size1",
            "KaTeX_Size2",
            "KaTeX_Size3",
            "KaTeX_Size4",
            "KaTeX_Typewriter",
        ],
    },
};
