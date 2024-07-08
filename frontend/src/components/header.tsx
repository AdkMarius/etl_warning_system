import React from "react";

function Header() {
    return (
        <>
            <div className="flex flex-row w-full h-24 justify-start items-center bg-primary-3 p-4">
                <div className="w-1/3">
                    <h1 className="font-montserrat text-white text-m-32 text-bold">Early Warning System</h1>
                </div>
            </div>
        </>
    );
}

export default Header;