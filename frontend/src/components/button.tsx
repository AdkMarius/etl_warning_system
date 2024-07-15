import React from "react";
import {ButtonProps} from "@/lib/props-definitions";


function Button(props: ButtonProps) {
    const {
        buttonText,
        handleClick
    } = props;

    return (
        <button
            type="button"
            className="w-[100px] h-[35px] rounded-md text-white text-k-16 bg-blue-600 opacity-75 hover:opacity-100 hover:cursor-pointer"
            onClick={handleClick}
        >
            {buttonText}
        </button>
    );
}

export default Button;