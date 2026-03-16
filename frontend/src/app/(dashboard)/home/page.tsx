"use client";

import {
  ArrowRightIcon,
  CaretDownIcon,
  MicrophoneIcon,
  PaperclipIcon,
} from "@phosphor-icons/react/dist/ssr";
import { examplePrompts } from "@/static/examplePrompts";
import { ExamplePromptCard } from "@/components/custom/examplePrompt";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import { zimnaApi } from "@/lib/api";

export default function Home() {
  const [showExamples, setShowExamples] = useState(false);
  const [inputValue, setInputValue] = useState("");

  const mutation = useMutation({
    mutationFn: (text: string) => zimnaApi.decomposeGoal(text),
    onSuccess: (data) => {
      console.log("Goal created!", data);
      setInputValue("");
      // TODO: trigger success toast and redirect
    },
    onError: (error: any) => {
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

        <div className="bg-linear-to-r from-blue-300 via-purple-300 via-50% to-purple-400 rounded-xl p-1">
          <div className="flex flex-col gap-3 p-1.5 rounded-lg bg-white">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={mutation.isPending}
              placeholder={
                mutation.isPending
                  ? "Zimna is decomposing..."
                  : "Ask whatever you want..."
              }
              className="[field-sizing-content] w-full min-h-10 max-h-48 p-2 outline-none border-none resize-none overflow-y-auto text-sm"
            ></textarea>

            <div className="flex justify-between items-center">
              <div className="flex gap-3 px-1">
                <button className="text-gray-500 hover:text-blue-700">
                  <MicrophoneIcon size={20} />
                </button>

                <button className="text-gray-500 hover:text-blue-700">
                  <PaperclipIcon size={20} />
                </button>
              </div>

              <div>
                <button
                  onClick={handleSubmit}
                  disabled={mutation.isPending}
                  className="p-2 rounded-lg text-blue-600 bg-linear-to-r from-blue-200 via-blue-200 via-20% to-purple-300 hover:text-blue-700"
                >
                  <ArrowRightIcon size={20} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
