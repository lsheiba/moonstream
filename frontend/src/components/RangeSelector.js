import React, { useEffect, useState, useRef } from "react";
import { Stack, Container, chakra } from "@chakra-ui/react";

const RangeSelector_ = ({
  className,
  ranges,
  onChange,
  initialRange,
  size,
}) => {
  const [range, setRange] = useState(initialRange ?? ranges[0]);
  const isFirstRun = useRef(true);

  useEffect(() => {
    if (isFirstRun.current) {
      isFirstRun.current = false;
    } else {
      onChange(range);
    }
  }, [range, onChange]);

  return (
    <Stack direction="row" className={className}>
      {ranges.map((item, idx) => {
        const isActive = item === range ? true : false;
        return (
          <Container
            key={`date-range-${className}-${idx}`}
            bgColor={isActive ? "secondary.900" : "primary.50"}
            color={!isActive ? "primary.900" : "primary.50"}
            boxShadow="sm"
            borderRadius="md"
            fontSize={size}
            fontWeight="600"
            onClick={() => setRange(item)}
            _hover={{
              bgColor: isActive ? "secondary.900" : "secondary.50",
            }}
            cursor="pointer"
          >
            {item}
          </Container>
        );
      })}
    </Stack>
  );
};

const RangeSelector = chakra(RangeSelector_);

export default RangeSelector;
