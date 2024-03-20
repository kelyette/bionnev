$('#start-restart').click(async () => {
    let b_state = await eel.sim_start()();

    $(this).text(b_state ? 'restart' : 'start');
})
$('#pause-resume').click(async () => {
    let b_state = await eel.sim_pause()();
    
    $(this).text(b_state ? 'restart' : 'start');
})
$('#manual-update').click()