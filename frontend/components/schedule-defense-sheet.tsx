"use client";

import * as React from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { format } from "date-fns";
import { CalendarIcon, Loader2Icon, ChevronDownIcon } from "lucide-react";
import { cn } from "@/lib/utils";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { Checkbox } from "@/components/ui/checkbox";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem } from "@/components/ui/command";

import { getProfessors, Professor, updateDefenseDetails } from "@/services/api"; // Import Professor and getProfessors


// Define the form schema
const formSchema = z.object({
  defense_date: z.date({
    required_error: "A defense date is required.",
  }),
  defense_time: z.string().min(1, "A defense time is required."),
  jury_members: z.array(z.number()).min(1, "At least one jury member must be selected."), // Array of professor IDs
});

export function ScheduleDefenseSheet({
  defense,
  onDefenseScheduled,
}: {
  defense: any; // Use the schema type later
  onDefenseScheduled: () => void;
}) {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      defense_date: defense.defense_date ? new Date(defense.defense_date) : undefined,
      defense_time: defense.defense_time || "",
      jury_members: defense.jury_members ? defense.jury_members.map((jm: any) => jm.professor_id) : [], // Pre-fill if available
    },
  });

  const [professors, setProfessors] = React.useState<Professor[]>([]);
  const [professorsLoading, setProfessorsLoading] = React.useState(true);
  const [professorsError, setProfessorsError] = React.useState<string | null>(null);

  React.useEffect(() => {
    async function loadProfessors() {
      try {
        const fetchedProfessors = await getProfessors();
        setProfessors(fetchedProfessors);
      } catch (e: any) {
        setProfessorsError(e.message);
      } finally {
        setProfessorsLoading(false);
      }
    }
    loadProfessors();
  }, []);

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    toast.info("Scheduling defense...", { id: "schedule-defense" });
    try {
      await updateDefenseDetails(defense.id, {
        status: 'accepted', // Automatically set to accepted on scheduling
        defense_date: format(values.defense_date, "yyyy-MM-dd"),
        defense_time: values.defense_time,
        jury_member_ids: values.jury_members, // Pass selected professor IDs
      });
      toast.success("Defense scheduled successfully!", { id: "schedule-defense" });
      onDefenseScheduled(); // Refresh the table
    } catch (error: any) {
      toast.error(error.message || "Failed to schedule defense.", { id: "schedule-defense" });
    }
  };

  if (professorsLoading) {
    return <div>Loading professors...</div>;
  }

  if (professorsError) {
    return <div>Error loading professors: {professorsError}</div>;
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="grid gap-4 py-4">
      {/* Date and Time input remain */}
      <div className="grid grid-cols-4 items-center gap-4">
        <Label htmlFor="defense_date" className="text-right">
          Date
        </Label>
        <div className="col-span-3">
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant={"outline"}
                className={cn(
                  "w-full justify-start text-left font-normal",
                  !form.watch("defense_date") && "text-muted-foreground"
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {form.watch("defense_date") ? (
                  format(form.watch("defense_date"), "PPP")
                ) : (
                  <span>Pick a date</span>
                )}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={form.watch("defense_date")}
                onSelect={(date) => form.setValue("defense_date", date || undefined)}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>
      <div className="grid grid-cols-4 items-center gap-4">
        <Label htmlFor="defense_time" className="text-right">
          Time
        </Label>
        <Input
          id="defense_time"
          type="time"
          className="col-span-3"
          {...form.register("defense_time")}
        />
      </div>

      {/* Professor assignment */}
      <div className="grid grid-cols-4 items-center gap-4">
        <Label htmlFor="jury_members" className="text-right">
          Jury Members
        </Label>
        <div className="col-span-3">
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-full justify-between">
                Select Professors
                <ChevronDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="p-0">
              <Command>
                <CommandInput placeholder="Search professors..." />
                <CommandEmpty>No professor found.</CommandEmpty>
                <CommandGroup>
                  {professors.map((professor) => (
                    <CommandItem key={professor.id} onSelect={() => {
                      const currentSelection = form.getValues("jury_members");
                      const newSelection = currentSelection.includes(professor.id)
                        ? currentSelection.filter((id) => id !== professor.id)
                        : [...currentSelection, professor.id];
                      form.setValue("jury_members", newSelection, { shouldValidate: true });
                    }}>
                      <Checkbox
                        checked={form.watch("jury_members")?.includes(professor.id)}
                        className="mr-2"
                      />
                      {`${professor.user.first_name} ${professor.user.last_name}`}
                    </CommandItem>
                  ))}
                </CommandGroup>
              </Command>
            </PopoverContent>
          </Popover>
        </div>
      </div>
      {form.formState.errors.jury_members && (
        <p className="col-span-4 text-right text-sm text-red-500">
          {form.formState.errors.jury_members.message}
        </p>
      )}


      <Button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting && (
          <Loader2Icon className="mr-2 h-4 w-4 animate-spin" />
        )}
        Schedule Defense
      </Button>
    </form>
  );
}