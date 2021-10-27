import React, { useEffect, useRef } from "react";
import { getLayout } from "../src/layouts/AppLayout";
import {
  Heading,
  Text,
  Stack,
  Fade,
  chakra,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
import Scrollable from "../src/components/Scrollable";

const Welcome = () => {
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Welcome to moonstream.to!`;
    }
  }, []);

  const scrollRef = useRef();

  return (
    <Scrollable>
      <Stack px="7%" pt={4} w="100%" spacing={4} ref={scrollRef}>
        {/* <StepProgress
          numSteps={ui.onboardingSteps.length}
          currentStep={ui.onboardingStep}
          colorScheme="blue"
          buttonCallback={progressButtonCallback}
          buttonTitles={[
            "Moonstream basics",
            "Setup subscriptions",
            "How to read stream",
          ]}
          style="arrows"
        /> */}

        {true && (
          <Fade in>
            <Stack spacing={4} pb={14}>
              <Stack
                px={[0, 12, null]}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Heading as="h4" size="md">
                  Greetings traveler!
                </Heading>
                <Text fontWeight="semibold" pl={2}>
                  We are very excited to see you onboard!
                </Text>

                <Text fontWeight="semibold" pl={2}>
                  Moonstream is a product which helps anyone participate in
                  decentralized finance.
                </Text>
                <Text fontWeight="semibold" pl={2}>
                  Moonstream is meant to give you critical insights you’ll need
                  to succeed in your crypto quest!
                </Text>
              </Stack>
              <Stack
                px={[0, 12, null]}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Accordion allowToggle>
                  <AccordionItem borderWidth={0}>
                    <h2>
                      <AccordionButton borderWidth={0}>
                        <Heading as="h4" size="md">
                          How does Moonstream work?
                        </Heading>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} borderWidth={0}>
                      <Stack direction="column">
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We run nodes
                          </Text>{" "}
                          - Get precise and accurate data by querying our
                          database. You’re getting the same data miners have
                          access to and you don’t have to maintain your own
                          node.
                        </chakra.span>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We crawl data
                          </Text>{" "}
                          - We analyze millions of transactions, data, and smart
                          contract code to link them together.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We provide data
                          </Text>
                          - You can fetch data through our front end or through
                          API.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            We analyze data
                          </Text>
                          - We find the most interesting information and
                          highlight it
                        </chakra.span>
                      </Stack>
                    </AccordionPanel>
                  </AccordionItem>
                </Accordion>
              </Stack>
              <Stack
                px={[0, 12, null]}
                // mt={24}
                bgColor="gray.50"
                borderRadius="xl"
                boxShadow="xl"
                py={4}
              >
                <Accordion allowToggle>
                  <AccordionItem borderWidth={0}>
                    <h2>
                      <AccordionButton borderWidth={0}>
                        <Heading as="h4" size="md">
                          UI navigation basics
                        </Heading>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} borderWidth={0}>
                      <Stack dir="column">
                        <Text fontWeight="semibold" pl={2}>
                          Use the sidebar on the left for navigation:
                        </Text>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Subscriptions
                          </Text>
                          Set up addresses you would like to monitor.{" "}
                          <i>
                            NB: Without any subscriptions, Moonstream will feel
                            quite empty!
                          </i>{" "}
                          No worries, we will help you set up your
                          subscriptions.
                          <i>
                            NB: Without setting up subscriptions moonstream will
                            have quite empty feel!{" "}
                          </i>{" "}
                          No worries, we will help you to set up your
                          subscriptions in the next steps!
                        </chakra.span>
                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Stream
                          </Text>{" "}
                          This view is similar to a bank statement. You can
                          define a date range and see what happened with your
                          subscriptions during that time. You can also apply
                          filters to it.
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Stream Entry
                          </Text>{" "}
                          - See a detailed view of stream cards with specific
                          and essential data, like methods called in smart
                          contracts etc
                        </chakra.span>

                        <chakra.span fontWeight="semibold" pl={2}>
                          <Text fontWeight="bold" display="inline">
                            Analytics
                          </Text>{" "}
                          - This section is under construction. Soon you will be
                          able to create dashboards there. Right now you can
                          fill out a form to tell us what analytical tools you’d
                          want to see. We’d really appreciate that :)
                        </chakra.span>
                      </Stack>
                    </AccordionPanel>
                  </AccordionItem>
                </Accordion>
              </Stack>
            </Stack>
          </Fade>
        )}

        {/* <ButtonGroup>
          <Button
            colorScheme="orange"
            leftIcon={<ArrowLeftIcon />}
            variant="outline"
            hidden={ui.onboardingStep === 0}
            disabled={ui.onboardingStep === 0}
            onClick={() => {
              ui.setOnboardingStep(ui.onboardingStep - 1);
              scrollRef?.current?.scrollIntoView();
            }}
          >
            Go back
          </Button>
          <Spacer />
          <Button
            colorScheme={
              ui.onboardingStep < ui.onboardingSteps.length - 1
                ? `orange`
                : `green`
            }
            variant={
              ui.onboardingStep < ui.onboardingSteps.length - 1
                ? `solid`
                : `outline`
            }
            rightIcon={
              ui.onboardingStep < ui.onboardingSteps.length - 1 && (
                <ArrowRightIcon />
              )
            }
            onClick={() => handleNextClick()}
          >
            {ui.onboardingStep < ui.onboardingSteps.length - 1
              ? `Next`
              : `Finish and move to stream`}
          </Button>
        </ButtonGroup> */}
      </Stack>
    </Scrollable>
  );
};
Welcome.getLayout = getLayout;
export default Welcome;
