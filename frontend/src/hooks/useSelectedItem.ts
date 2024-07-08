import {DataModel} from "@/lib/datas-definition";
import {useImmer} from "use-immer";

function useSelectedItem(initialValue: DataModel) {

    const [selectedItem, setSelectedItem] = useImmer(initialValue);

    const handleClick = (item: DataModel | null) => {
        if (item) {
            setSelectedItem(draft => {
                draft.id = item.id;
                draft.code = item.code;
                draft.displayName = item.displayName;
            });
        }
    };

    return {
        selectedItem: selectedItem,
        handleClick: handleClick
    };
}

export default useSelectedItem;