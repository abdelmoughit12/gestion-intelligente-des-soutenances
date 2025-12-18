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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { getProfessors, Professor, updateDefenseDetails, assignJuryMember } from "@/services/api"; // Import Professor and getProfessors

// Define the enum for JuryRole
const JuryRole = z.enum(["president", "secretary", "examiner", "member"]);

// Define the form schema
const formSchema = z.object({
  defense_date: z.date({
    required_error: "A defense date is required.",
  }),
  defense_time: z.string().min(1, "A defense time is required."),
  jury_members: z.array(z.object({
    professorId: z.number(),
    role: JuryRole,
  })).min(1, "At least one jury member must be selected."),
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
      jury_members: defense.jury_members ? defense.jury_members.map((jm: any) => ({ professorId: jm.professor_id, role: jm.role || 'examiner' })) : [], // Pre-fill if available
    },
  });

  const [professors, setProfessors] = React.useState<Professor[]>([]);
  const [professorsLoading, setProfessorsLoading] = React.useState(true);
  const [professorsError, setProfessorsError] = React.useState<string | null>(null);
  const [isJuryPopoverOpen, setJuryPopoverOpen] = React.useState(false);

  const toggleProfessor = (professorId: number) => {
    const currentSelection = form.getValues("jury_members");
    const existingMember = currentSelection.find(member => member.professorId === professorId);

    if (existingMember) {
      form.setValue("jury_members", currentSelection.filter(member => member.professorId !== professorId), { shouldValidate: true });
    } else {
      form.setValue("jury_members", [...currentSelection, { professorId, role: "examiner" }], { shouldValidate: true });
    }
  };

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
    toast.info("Scheduling defense and assigning jury...", { id: "schedule-defense" });
    try {
      // Step 1: Update defense status, date, and time
      await updateDefenseDetails(defense.id, {
        status: 'accepted',
        defense_date: format(values.defense_date, "yyyy-MM-dd"),
        defense_time: values.defense_time,
      });

      // Step 2: Assign each jury member with a specific role
      const juryAssignmentPromises = values.jury_members.map(({ professorId, role }) => {
        return assignJuryMember(defense.id, professorId, role);
      });
      await Promise.all(juryAssignmentPromises);

      toast.success("Defense scheduled and jury assigned successfully!", { id: "schedule-defense" });
      onDefenseScheduled(); // Refresh the table
    } catch (error: any) {
      toast.error(error.message || "Failed to schedule defense.", { id: "schedule-defense" });
    }
  };

  const juryMembers = form.watch("jury_members");

  const professorItems = React.useMemo(() => {
    return professors
      .filter((p) => p.user && p.user.id != null)
      .map((professor) => (
        <CommandItem
          key={professor.user.id}
          value={professor.user.id.toString()}
          onSelect={() => toggleProfessor(professor.user.id)}
        >
          <Checkbox
            checked={juryMembers?.some(member => member.professorId === professor.user.id)}
            className="mr-2"
          />
          {`${professor.user.first_name} ${professor.user.last_name}`}
        </CommandItem>
      ));
  }, [professors, juryMembers]);

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
          <Popover open={isJuryPopoverOpen} onOpenChange={setJuryPopoverOpen}>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-full justify-between">
                Select Professors
                <ChevronDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-96 p-0" align="start">
              <Command>
                <CommandInput placeholder="Search professors..." />
                <CommandEmpty>No professor found.</CommandEmpty>
                <CommandGroup>
                  {professorItems}
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

      {juryMembers.map((member, index) => {
        const professor = professors.find(p => p.user.id === member.professorId);
        return (
          <div key={member.professorId} className="grid grid-cols-4 items-center gap-4">
            <Label className="text-right">{professor?.user.first_name} {professor?.user.last_name}</Label>
            <div className="col-span-3">
              <Select
                value={member.role}
                onValueChange={(value) => {
                  const newJuryMembers = [...juryMembers];
                  newJuryMembers[index].role = value as z.infer<typeof JuryRole>;
                  form.setValue("jury_members", newJuryMembers, { shouldValidate: true });
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select a role" />
                </SelectTrigger>
                <SelectContent>
                  {JuryRole.options.map(role => (
                    <SelectItem key={role} value={role}>
                      {role.charAt(0).toUpperCase() + role.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        );
      })}

      <Button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting && (
          <Loader2Icon className="mr-2 h-4 w-4 animate-spin" />
        )}
        Schedule Defense
      </Button>
    </form>
  );
}