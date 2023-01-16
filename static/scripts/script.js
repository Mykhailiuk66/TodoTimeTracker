let alerts = document.getElementsByClassName("alert");

for (let i = 0; i < alerts.length; i++) {
	setTimeout(
		(el) => {
			el.remove();
		},
		5000,
		alerts[i]
	);
}

let taskCheckers = document.getElementsByClassName("task-checker");

for (let i = 0; i < taskCheckers.length; i++) {
	taskCheckers[i].addEventListener("click", (e) => {
		let url = e.target.dataset.url;
		let id = e.target.dataset.id;

		fetch(url, {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		})
			.then((response) => response.json())
			.then((data) => {
				// console.log(data)
				formatTask(id, data.checked);
			});
	});
}

let taskDeleteBtns = document.getElementsByClassName("task-delete");

for (let i = 0; i < taskDeleteBtns.length; i++) {
	taskDeleteBtns[i].addEventListener("click", (e) => {
		let url = e.target.dataset.url;
		let id = e.target.dataset.id;

		fetch(url, {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		}).then(() => {
			let task = document.getElementsByClassName(`task-${id}`)[0];

			task.nextElementSibling.remove();
			task.remove();
		});
	});
}

function formatTask(id, checked) {
	let task = document.getElementsByClassName(`task-${id}`)[0];
	let taskCancelBtn = task.getElementsByClassName("task-cancel-li")[0];

	if (checked) {
		task.classList.remove("task-done-False");
		task.classList.add("task-done-True");

		taskCancelBtn.classList.remove("btn-hide");
	} else {
		task.classList.remove("task-done-True");
		task.classList.add("task-done-False");

		taskCancelBtn.classList.add("btn-hide");

		taskCheckbox = task.getElementsByClassName("checkbox-input")[0];
		// console.log(taskCheckbox);
		taskCheckbox.checked = false;
	}
}

///////////////////////////

let timelineDeleteBtns = document.getElementsByClassName("timeline-delete");

for (let i = 0; i < timelineDeleteBtns.length; i++) {
	timelineDeleteBtns[i].addEventListener("click", (e) => {
		let url = e.target.dataset.url;
		let id = e.target.dataset.id;

		fetch(url, {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		}).then(() => {
			let timeline = document.getElementsByClassName(`timeline-${id}`)[0];

			timeline.nextElementSibling.remove();
			timeline.remove();
		});
	});
}

let elapsedTime = document.getElementsByClassName("elapsed-time");
for (let i = 0; i < elapsedTime.length; i++) {
	let startTime = new Date(elapsedTime[i].dataset.starttime);

	setInterval(updateTime, 500, startTime, elapsedTime[i]);
}

function updateTime(startTime, element) {
	let elapsedTime = Date.now() - startTime;

	let tempTime = elapsedTime;
	tempTime = Math.floor(tempTime / 1000);
	let seconds = tempTime % 60;
	if (seconds < 10) seconds = "0" + seconds;

	tempTime = Math.floor(tempTime / 60);
	let minutes = tempTime % 60;
	if (minutes < 10) minutes = "0" + minutes;

	tempTime = Math.floor(tempTime / 60);
	let hours = tempTime % 60;
	if (hours < 10) hours = "0" + hours;

	let time = hours + " : " + minutes + " : " + seconds;
	element.innerText = time;
	// $("#time").text(time);
}

function formatPeriod(element) {
	let period = element.innerText;

	splitPeriod = period.split(":");

	for (let i = 0; i < splitPeriod.length; i++) {
		if (splitPeriod[i].length < 2) {
			splitPeriod[i] = "0" + splitPeriod[i];
		} else if (splitPeriod[i].length > 2) {
			splitPeriod[i] = splitPeriod[i].slice(0, 2);
		}
	}

	let formattedPeriod = splitPeriod.join(":");

	element.innerText = formattedPeriod;
}

let periods = document.getElementsByClassName("period");
for (let i = 0; i < periods.length; i++) {
	formatPeriod(periods[i]);
}
