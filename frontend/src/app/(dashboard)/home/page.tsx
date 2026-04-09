"use client";

import { CaretDownIcon } from "@phosphor-icons/react/dist/ssr";
import { examplePrompts } from "@/static/examplePrompts";
import { ExamplePromptCard } from "@/components/custom/examplePrompt";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import { goalsApi } from "@/lib/api/goals";
import { Goal } from "@/lib/api/types";
import { PromptField } from "@/components/custom/promptField";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const [showExamples, setShowExamples] = useState(false);
  const [inputValue, setInputValue] = useState("");

  const mutation = useMutation({
    mutationFn: (text: string) => goalsApi.decompose(text),
    onSuccess: (data: Goal[]) => {
      console.log("Goal created!", data);
      setInputValue("");

      if (data && data.length > 0) {
        const primaryGoalId = data[0].id;

        // Redirect user to the console for this specific goal
        router.push(`/console/${primaryGoalId}`);
      }
    },
    onError: (error: Error) => {
      alert(error.message);
    },
  });

  const handleSubmit = async () => {
    if (inputValue.trim()) {
      mutation.mutate(inputValue);
    }
  };

  const handleExampleClick = (text: string) => {
    setInputValue(text);
    setShowExamples(false);
  };

  return (
    <section className="flex justify-center items-center w-full">
      <div className="space-y-3 w-full lg:w-3/5">
        <div className="space-y-2">
          <header className="flex flex-col text-3xl lg:text-4xl">
            <b className="bg-linear-to-r from-blue-500 via-purple-500 via-40% to-purple-700 bg-clip-text text-transparent w-fit">
              Hi there, User
            </b>
            <b className="bg-linear-to-r from-blue-500 via-purple-500 via-40% to-purple-700 bg-clip-text  text-transparent w-fit">
              Let&apos;s get productive!
            </b>
          </header>

          <div>
            <p className="text-sm text-gray-500">
              I&apos;m here to assist you on your journey to achieveing your
              goals, whatever they are.
            </p>

            <button
              onClick={() => setShowExamples(!showExamples)}
              className="flex gap-1 items-center text-sm text-gray-500 hover:text-blue-700"
            >
              Check out our example prompts
              <CaretDownIcon
                size={18}
                className={cn(
                  "transition-transform duration-300",
                  showExamples ? "rotate-180" : "rotate-0",
                )}
              />
            </button>
          </div>

          {showExamples && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
              {examplePrompts.map((item, index) => (
                <ExamplePromptCard
                  key={index}
                  text={item.prompt}
                  onClick={() => handleExampleClick(item.prompt)}
                />
              ))}
            </div>
          )}
        </div>

        <PromptField
          value={inputValue}
          isPending={mutation.isPending}
          disabled={mutation.isPending}
          onChange={(e) => setInputValue(e.target.value)}
          onSubmit={handleSubmit}
        />
      </div>
    </section>
  );
}
