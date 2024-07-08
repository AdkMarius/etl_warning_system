import React from "react";
import clsx from "clsx";
import {ArrowUpRightIcon} from "@heroicons/react/24/solid";

export type ButtonProps = {
    buttonText: string;
    handleClick: () => void;
}
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