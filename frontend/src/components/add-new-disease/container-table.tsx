'use client';

import React, {useEffect, useState} from "react";
import {Table} from "@/components";
import useSelectedItem from "@/hooks/useSelectedItem";
import {ArrowUpRightIcon} from "@heroicons/react/24/solid";
import clsx from "clsx";
import {DataModel, SelectedData} from "@/lib/datas-definition";
import {CustomDialog} from "@/components";
import {ErrorType, SubmitResponse} from "@/lib/props-definitions";

function ContainerTable() {
    const initialValue: DataModel = {
        id: "",
        code: "",
        displayName: ""
    };

    const selectedDiseaseProps = useSelectedItem(initialValue);
    const selectedIndicatorProps = useSelectedItem(initialValue);
    const selectedDataElementProps = useSelectedItem(initialValue);

    const [status, setStatus] = useState<ErrorType>("empty");
    const [message, setMessage] = useState<string>("");
    const [open, setOpen] = React.useState<boolean>(false);


    const isDisabled = !selectedDiseaseProps.selectedItem.id ||
        !selectedIndicatorProps.selectedItem.id || !selectedDataElementProps.selectedItem.id;

    const handleSubmit = async (): Promise<void> => {
        setStatus("submitting");

        const selectedDisease = selectedDiseaseProps.selectedItem;
        const selectedIndicator = selectedIndicatorProps.selectedItem;
        const selectedDataElement = selectedDataElementProps.selectedItem;

        const selectedData: SelectedData = {
            disease: {
                id: selectedDisease.id,
                code: selectedDisease.code as string,
                displayName: selectedDisease.displayName
            },
            indicator: {
                id: selectedIndicator.id,
                displayName: selectedIndicator.displayName
            },
            dataElement: {
                id: selectedDataElement.id,
                displayName: selectedDataElement.displayName
            }
        }

        try {
            const res = await fetch('/api/send-selected-data', {
                method: 'POST',
                body: JSON.stringify(selectedData),
                headers: {
                    'Content-type': 'application/json'
                }
            });
            if (res.ok) {
                const result: SubmitResponse = await res.json();
                if (result.httpStatusCode === 200) {
                    setStatus("success");
                    setMessage(result.message)
                } else {
                    setStatus("error");
                    setMessage(result.message)
                }
            }
        } catch (error) {
            setStatus("error");
            setMessage("Error occurs. Please try again!")
            console.error(error);
        }
    }

    useEffect(() => {
        if (status === "success" || status === "error") {
            setOpen(false);
        }

        if (status === "success") {
            selectedDiseaseProps.handleClick(null);
            selectedIndicatorProps.handleClick(null);
            selectedDataElementProps.handleClick(null);

            setTimeout(() => setStatus("empty"), 3000);
        }
    }, [status])

    return (
        <>
            <section className="flex flex-col w-full">
                <div className="flex flex-row justify-between w-full p-8 gap-x-10">
                    <Table
                        dType="diseases"
                        placeholder="Search in diseases"
                        status={status}
                        headingChildren="Diseases"
                        {...selectedDiseaseProps}
                    />
                    <Table
                        dType="indicators"
                        placeholder="Search in indicators"
                        status={status}
                        headingChildren="Indicators"
                        {...selectedIndicatorProps}
                    />
                    <Table
                        dType="dataElements"
                        placeholder="Search in data elements"
                        status={status}
                        headingChildren="Data Elements"
                        {...selectedDataElementProps}
                    />
                </div>

                <div className="flex flex-col w-full items-end p-8 gap-y-4">
                    <div className="">
                        <button
                            type="button"
                            className={clsx(
                                'flex justify-center items-center text-white font-karla text-k-20 w-[250px] h-[64px] rounded-lg',
                                'focus-visible:outline-none',
                                {
                                    'bg-gray-300 hover:bg-gray-300 cursor-not-allowed': isDisabled,
                                    'bg-primary-3 opacity-75 hover:cursor-pointer hover:opacity-100': !isDisabled
                                }
                            )}
                            onClick={handleSubmit}
                            disabled={isDisabled}
                        >
                            <span className="block">Submit</span>
                            <ArrowUpRightIcon className='size-6 ml-4'/>
                        </button>
                    </div>
                    <div className="">
                        { status === "success" && (
                            <p className="font-karla text-k-16 font-bold text-green-600">{message}</p>
                        )}

                        { status === "error" && (
                            <p className="font-karla text-k-16 font-bold text-red-600">{message}</p>
                        )}
                    </div>
                </div>
                { status === "submitting" && (
                    <CustomDialog isOpen={true} />
                )}
            </section>
        </>
    );
}

export default ContainerTable;