import React from "react";
import { ResponsiveLineCanvas } from "@nivo/line";

const Report = ({ data }) => {
  const commonProperties = {
    animate: false,
    enableSlices: "x",
  };

  const xyData = data.map((item) => {
    return { x: item.date, y: item.count };
  });

  function generateCumulativeSum(sum) {
    function cumulativeSum(item) {
      sum += item.count;
      return { x: item.date, y: sum };
    }
    return cumulativeSum;
  }

  xyCumulativeData = xyData.map(generateCumulativeSum(0));

  const plotData = [{ id: "1", data: xyCumulativeData }];

  return (
    <ResponsiveLineCanvas
      {...commonProperties}
      data={plotData}
      isInteractive={true}
      xScale={{
        type: "time",
        format: "%Y-%m-%d %H",
        useUTC: false,
        precision: "hour",
      }}
      xFormat="time:%Y-%m-%d %H"
      yScale={{
        type: "linear",
      }}
      axisLeft={{
        orient: "left",
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legendOffset: -40,
        legendPosition: "middle",
      }}
      axisBottom={{
        format: "%b %d",
        tickValues: "every 7 day",
        tickRotation: 90,
      }}
      curve="step"
      enablePointLabel={false}
      pointSize={0}
      colors="#fd671b"
      pointBorderWidth={1}
      pointBorderColor={{
        from: "color",
        modifiers: [["darker", 0.3]],
      }}
      useMesh={true}
      enableSlices={false}
      enableGridX={true}
      enableGridY={true}
    />
  );
};

export default Report;
