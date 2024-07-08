import React, {Fragment} from "react";
import {Skeleton} from "@mui/material";

function DataSkeletons() {
    return (
      <div className="flex flex-col">
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
          <Skeleton animation="wave" width={400} height={40} variant="rectangular" className="ml-4 mb-4" />
      </div>
    );
}

export default DataSkeletons;