'use client';

import React from "react";
import {DataModel} from "@/lib/datas-definition";
import clsx from "clsx";

export type TableDataProps = {
    status: string;
    items: DataModel[];
    selectedItem: DataModel;
    handleClick: (item: DataModel) => void;
}

function TableData(props: TableDataProps) {
    const {
        status,
        items,
        selectedItem,
        handleClick
    } = props;

    return (
        <>
            {items.map(item => (
                <div
                    key={item.id}
                    className={clsx(
                        'w-full p-4 hover:cursor-pointer',
                        {
                            'bg-primary-3 hover:bg-primary-3 text-white text-bold': item.id === selectedItem.id,
                            'hover:bg-secondary-1': item.id !== selectedItem.id
                        }
                    )}
                    onClick={() => {
                        handleClick(item);
                    }}
                >
                    {item.code ? (
                        <span className="font-karla text-k-16">{item.displayName} ({item.code})</span>
                    ) : (
                        <span className="font-karla text-k-16">{item.displayName}</span>
                    )}
                </div>
            ))}
        </>
    );
};

export default TableData;